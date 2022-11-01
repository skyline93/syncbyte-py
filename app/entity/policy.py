from core.db import get_session

from .entity import Entity


class BackupPolicy(Entity):
    async def _load_from_db(self, **kwargs):
        session = kwargs.get("session")
        if session is None:
            session = get_session()

    def _load_from_model(self, m):
        self.id = m.id
        self.retention = m.retention
        self.is_compress = m.is_compress
        self.resource_id = m.resource_id


async def create_policy(
    retention,
    is_compress,
    schedule_type,
    schedule_options,
    resource_name,
    resource_type,
    resource_options,
):
    session = get_session()

    result = await session.execute(
        select(models.Resource).where(models.Resource.name == resource_name)
    )
    resource = result.first()
    if resource is not None:
        raise Exception("resource is exist already")

    resource = models.Resource(name=resource_name, resource_type=resource_type)

    if resource_type == "database":
        database = models.Database(resource=resource, **resource_options)

    policy = models.BackupPolicy(
        retention=retention,
        is_compress=is_compress,
        status="implemented",
        resource=resource,
    )

    backup_schedule = models.BackupSchedule(
        schedule_type=schedule_type, backup_policy=policy, **schedule_options
    )

    session.add_all([resource, database, policy, backup_schedule])

    await session.commit()
