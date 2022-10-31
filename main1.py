import asyncio
import logging

from sqlalchemy import Column, String
from sqlalchemy.future import select
from sqlalchemy.engine import Result
from sqlalchemy.orm import Session

from pkg.worker import Worker, BaseTask
from core import db, policy
from core.entity import Host
from core.constant import HostType
from core.scheduling import schedule_backup_job

logging.basicConfig(
    filename="app.log",
    level=logging.DEBUG,
    format="[%(asctime)s] %(levelname)s [:%(lineno)d]: %(message)s",
)
logger = logging.getLogger(__name__)
stream_handler = logging.StreamHandler()
logger.addHandler(stream_handler)


class MyTask(BaseTask):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def run(self):
        await asyncio.sleep(30)
        logger.debug(f"hello, my name is {self.name}")


async def worker_main():
    worker = Worker(logger=logger)
    worker.run_in_background()

    tasks = []
    for i in range(0, 50):
        task = MyTask(f"task{i}")
        tasks.append(worker.send_task(task))

    await asyncio.gather(*tasks)


async def sqlalchemy_main():
    await db.init(
        "postgresql+asyncpg://syncbyte:lyp82nLF!?@192.168.1.131:5432/syncbytepy"
    )

    retention = 7
    is_compress = True
    resource_name = "core_cms"
    resource_type = "database"
    schedule_type = "cron"

    resource_options = {
        "db_type": "postgresql",
        "version": "14.5",
        "server": "192.168.1.131",
        "port": 5432,
        "user": "syncbyte",
        "password": "lyp82nlF!?",
        "db_name": "syncbytepy",
    }

    schedule_options = {"cron": "*/2 * * * *"}

    await policy.create_policy(
        retention,
        is_compress,
        schedule_type,
        schedule_options,
        resource_name,
        resource_type,
        resource_options,
    )


async def add_host():
    await db.init(
        "postgresql+asyncpg://syncbyte:lyp82nLF!?@192.168.1.131:5432/syncbytepy"
    )

    await Host.add("192.168.1.139", "VMDEV", HostType.BACKUP.value)


async def schedule_job():
    await db.init(
        "postgresql+asyncpg://syncbyte:lyp82nLF!?@192.168.1.131:5432/syncbytepy"
    )
    await schedule_backup_job(1)


if __name__ == "__main__":
    # asyncio.run(worker_main())
    # asyncio.run(sqlalchemy_main())
    # asyncio.run(add_host())
    asyncio.run(schedule_job())
