from typing import Optional

import grpc

from takler.server.protocol import takler_pb2, takler_pb2_grpc
from takler.logging import get_logger
from takler.server.scheduler import Scheduler


service_logger = get_logger("server.service")


class TaklerService(takler_pb2_grpc.TaklerServerServicer):
    def __init__(self, scheduler: Scheduler):
        self.scheduler = scheduler
        self.host = '[::]'  # type: str
        self.port = 50051  # type: int
        self.grpc_server = None  # type: Optional[grpc.aio.Server]

    @property
    def listen_address(self) -> str:
        return f'{self.host}:{self.port}'

    async def start(self):
        self.grpc_server = grpc.aio.server()
        takler_pb2_grpc.add_TaklerServerServicer_to_server(self, self.grpc_server)
        self.grpc_server.add_insecure_port(self.listen_address)
        await self.grpc_server.start()
        service_logger.info(f"service started: {self.listen_address}")

    async def run(self):
        await self.grpc_server.wait_for_termination()

    async def RunInitCommand(self, request, context):
        node_path = request.child_options.node_path
        task_id = request.task_id

        service_logger.info(f"Init: {node_path} with {task_id}")
        await self.scheduler.run_command_init(node_path, task_id)
        return takler_pb2.ServiceResponse(
            flag=0,
            message="",
        )

    async def RunCompleteCommand(self, request, context):
        node_path = request.child_options.node_path
        service_logger.info(f"Complete: {node_path}")
        self.scheduler.run_command_complete(node_path)

        return takler_pb2.ServiceResponse(
            flag=0,
            message="",
        )

    async def RunAbortCommand(self, request, context):
        node_path = request.child_options.node_path
        service_logger.info(f"Abort: {node_path}")
        self.scheduler.run_command_abort(node_path)

        return takler_pb2.ServiceResponse(
            flag=0,
            message="",
        )

    async def RunShowRequest(self, request, context):
        output = self.scheduler.handle_show_request()
        return takler_pb2.ShowResponse(
            output=output
        )
