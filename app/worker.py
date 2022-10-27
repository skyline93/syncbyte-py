import asyncio
import logging

logger = logging.getLogger(__name__)


class Worker:
    def __init__(self, concurrent=5):
        self.concurrent = concurrent
        self.queue = asyncio.Queue(maxsize=1)

    async def _executor(self):
        while True:
            task = await self.queue.get()
            await task.run()

    async def _run(self):
        async with asyncio.TaskGroup() as tg:
            for _ in range(0, self.concurrent):
                tg.create_task(self._executor())

            logger.debug(f"init worker, concurrent: {self.concurrent}")

    async def run(self):
        await self._run()

    def run_in_background(self):
        asyncio.create_task(self._run())

    async def send_task(self, task):
        await self.queue.put(task)


class BaseTask:
    def __init__(self, name):
        self.name = name

    async def run(self):
        raise
