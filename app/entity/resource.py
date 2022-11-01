from sqlalchemy.future import select

from core.db import models, get_session
from core.constant import ResourceType
from core.exceptions import NotSupport

from .entity import Entity


class Resource(Entity):
    def __init__(self, id, **kwargs):
        super().__init__(id, **kwargs)

    async def _load_from_db(self, **kwargs):
        session = kwargs.get("session")
        if session is None:
            session = get_session()

        result = await session.execute(
            select(models.Resource).where(models.Resource.id == self.id)
        )
        resource = result.scalars().first()

        self.name = resource.name
        self.type = resource.resource_type

        if resource.resource_type == ResourceType.DATABASE.value:
            result = await session.execute(
                select(models.Database).where(models.Database.resource_id == self.id)
            )
            database = result.scalars().first()

            self.options = {
                "db_type": database.db_type,
                "version": database.version,
                "server": database.server,
                "port": database.port,
                "user": database.user,
                "password": database.password,
                "db_name": database.db_name,
            }
        else:
            raise NotSupport("not support resource type")
