from pkg.rds import get_session
from core.db import models


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

    resource = session.get(models.Resource, {"name": resource_name})
    # if 

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
