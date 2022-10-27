import asyncio
import logging

from app.worker import Worker, BaseTask

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
        logger.debug(f"hello, my name is {self.name}")
        await asyncio.sleep(1)


async def main():
    worker = Worker(concurrent=500)
    worker.run_in_background()

    tasks = []
    for i in range(0, 5000):
        task = MyTask(f"task{i}")
        tasks.append(worker.send_task(task))

    await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(main())
