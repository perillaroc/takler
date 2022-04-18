from takler.server.protocol import takler_pb2
from takler.server.protocol.takler_pb2_grpc import TaklerServerServicer


class TaklerServer(TaklerServerServicer):
    async def RunInitCommand(self, request, context):
        node_path = request.child_options.node_path
        task_id = request.task_id

        print(f"INIT: {node_path} with {task_id}")
        return takler_pb2.ServiceResponse(
            flag=0,
            message="",
        )
