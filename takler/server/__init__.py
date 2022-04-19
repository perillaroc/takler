import asyncio
from typing import Optional, Union

from takler.core import Bunch
from .scheduler import Scheduler
from .network_service import TaklerService


class TaklerServer:
    def __init__(self):
        self.bunch = Bunch()  # type: Bunch
        self.scheduler = Scheduler(bunch=self.bunch)
        self.network_service = TaklerService(scheduler=self.scheduler)

    async def start(self):
        await self.scheduler.start()
        await self.network_service.start()

    async def run(self):
        loop = asyncio.get_running_loop()
        loop.create_task(self.network_service.run())

        await self.scheduler.run()
