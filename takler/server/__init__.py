import asyncio

from takler.core import Bunch
from takler.logging import get_logger

from .scheduler import Scheduler
from .network_service import TaklerService


logger = get_logger("server")


class TaklerServer:
    def __init__(self, host: str = None, port: int = None):
        self.bunch: Bunch = Bunch()
        self.scheduler: Scheduler = Scheduler(bunch=self.bunch)
        self.network_service: TaklerService = TaklerService(
            scheduler=self.scheduler, host=host, port=port
        )

    async def start(self):
        logger.info("start server...")
        await self.scheduler.start()
        await self.network_service.start()
        logger.info("start server...done")

    async def run(self):
        """
        Run services:

        * run network service
        * run scheduler
        """
        loop = asyncio.get_running_loop()
        loop.create_task(self.network_service.run())

        await self.scheduler.run()

    async def stop(self):
        """
        Stop all services:

        * stop network service
        * stop scheduler
        """
        await self.network_service.stop()
        await self.scheduler.stop()
