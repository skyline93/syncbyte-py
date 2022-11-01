from sqlalchemy.future import select

from core.db import models, get_session
from core.constant import ScheduleJobStatus
from core.entity import Resource, Host


async def schedule_backup_job(policy_id):
    session = get_session()

    result = await session.execute(
        select(models.BackupPolicy).where(models.BackupPolicy.id == policy_id)
    )
    policy = result.scalars().first()

    if policy is None:
        raise Exception("backup policy not found")

    resource = await Resource(policy.resource_id)
    host = await Host.get_backup_host()

    job = models.ScheduledJob(
        status=ScheduleJobStatus.QUEUED.value,
        host_id=host.id,
        resource_id=policy.resource_id,
        backup_policy_id=policy.id,
        args={"resource_options": resource.options},
    )

    session.add(job)

    await session.commit()

    return job.id
