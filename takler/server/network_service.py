from typing import Optional

import grpc

from takler.server.protocol import takler_pb2, takler_pb2_grpc
from takler.logging import get_logger
from takler.server.scheduler import Scheduler


logger = get_logger("server.service")


class TaklerService(takler_pb2_grpc.TaklerServerServicer):
    """
    RPC 服务端，响应客户端命令。

    Attributes
    ----------
    scheduler : Scheduler
        A link to the scheduler. Service use it to run commands.
    host : str
        Service host
    port : int
        Service port
    """
    def __init__(self, scheduler: Scheduler, host: str = None, port: int = None):
        self.scheduler = scheduler
        if host is None:
            host = "[::]"
        if port is None:
            port = 33083
        self.host = host  # type: str
        self.port = port  # type: int
        self.grpc_server = None  # type: Optional[grpc.aio.Server]

    @property
    def listen_address(self) -> str:
        """
        str: gRPC server's listen address
        """
        return f'{self.host}:{self.port}'

    async def start(self):
        """
        Start gRPC server.
        """
        self.grpc_server = grpc.aio.server()
        takler_pb2_grpc.add_TaklerServerServicer_to_server(self, self.grpc_server)
        self.grpc_server.add_insecure_port(self.listen_address)
        await self.grpc_server.start()
        logger.info(f"service started: {self.listen_address}")

    async def run(self):
        """
        Run service.
        """
        await self.grpc_server.wait_for_termination()

    async def stop(self):
        logger.info("service shutting down..")
        await self.grpc_server.stop(5)
        logger.info("service shutting down..done")

    async def RunInitCommand(self, request, context):
        node_path = request.child_options.node_path
        task_id = request.task_id

        logger.info(f"Init: {node_path} with {task_id}")
        await self.scheduler.run_command_init(node_path, task_id)
        return takler_pb2.ServiceResponse(
            flag=0,
            message="",
        )

    async def RunCompleteCommand(self, request, context):
        node_path = request.child_options.node_path
        logger.info(f"Complete: {node_path}")
        self.scheduler.run_command_complete(node_path)

        return takler_pb2.ServiceResponse(
            flag=0,
            message="",
        )

    async def RunAbortCommand(self, request, context):
        node_path = request.child_options.node_path
        logger.info(f"Abort: {node_path}")
        self.scheduler.run_command_abort(node_path)

        return takler_pb2.ServiceResponse(
            flag=0,
            message="",
        )

    async def RunRequeueCommand(self, request, context):
        node_path = request.node_path
        logger.info(f"Requeue: {node_path}")
        self.scheduler.run_command_requeue(node_path)

        return takler_pb2.ServiceResponse(
            flag=0,
            message="",
        )

    async def RunShowRequest(self, request, context):
        output = self.scheduler.handle_request_show()
        return takler_pb2.ShowResponse(
            output=output
        )
