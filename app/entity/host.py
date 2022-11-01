from sqlalchemy.future import select

from core.db import models, get_session
from core.constant import HostType

from .entity import Entity


class Host(Entity):
    async def _load_from_db(self, **kwargs):
        session = kwargs.get("session")
        if session is None:
            session = get_session()

        result = await session.execute(
            select(models.Host).where(models.Host.id == self.id)
        )
        m = result.scalars().first()

        await session.commit()

        self._load_from_model(m)

    def _load_from_model(self, m):
        self.id = m.id
        self.ip = m.ip
        self.name = m.hostname
        self.type = m.host_type

        return self

    @classmethod
    async def add(cls, ip, hostname, host_type, **kwargs):
        session = kwargs.get("session")
        if session is None:
            session = get_session()

        m = models.Host(ip=ip, hostname=hostname, host_type=host_type)
        session.add(m)

        await session.commit()

        self = cls(m.id)
        return self

    @classmethod
    async def get_backup_host(cls, **kwargs):
        session = kwargs.get("session")
        if session is None:
            session = get_session()

        result = await session.execute(
            select(models.Host).where(models.Host.host_type == HostType.BACKUP.value)
        )

        m = result.scalars().first()
        await session.commit()

        self = await cls(m.id)
        return self
