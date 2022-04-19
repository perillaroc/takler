from takler.server.protocol import takler_pb2
from takler.server.protocol.takler_pb2_grpc import TaklerServerServicer
from takler.logging import get_logger


service_logger = get_logger("server.service")


class TaklerService(TaklerServerServicer):
    async def RunInitCommand(self, request, context):
        node_path = request.child_options.node_path
        task_id = request.task_id

        service_logger.info(f"Init: {node_path} with {task_id}")
        return takler_pb2.ServiceResponse(
            flag=0,
            message="",
        )

    async def RunCompleteCommand(self, request, context):
        node_path = request.child_options.node_path
        service_logger.info(f"Complete: {node_path}")

        return takler_pb2.ServiceResponse(
            flag=0,
            message="",
        )

    async def RunAbortCommand(self, request, context):
        node_path = request.child_options.node_path
        service_logger.info(f"Abort: {node_path}")

        return takler_pb2.ServiceResponse(
            flag=0,
            message="",
        )
