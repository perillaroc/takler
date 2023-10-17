from typing import Optional, List, Dict
import asyncio

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
        self.scheduler: Scheduler = scheduler
        if host is None:
            host = "[::]"
        if port is None:
            port = 33083
        self.host: str = host
        self.port: int = port
        self.grpc_server: Optional[grpc.aio.Server] = None

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
        Wait until gRPC server is terminated.
        """
        await self.grpc_server.wait_for_termination()

    async def stop(self):
        """
        Stop gRPC server with time limit.
        """
        logger.info("service shutting down..")
        await self.grpc_server.stop(5)
        logger.info("service shutting down..done")

    # Child command -----------------------------------------------------

    async def RunCommandInit(self, request, context):
        node_path = request.child_options.node_path
        task_id = request.task_id

        logger.info(f"Init: {node_path} with {task_id}")
        await self.scheduler.run_command_init(node_path, task_id)
        return takler_pb2.ServiceResponse(
            flag=0,
            message="",
        )

    async def RunCommandComplete(self, request, context):
        node_path = request.child_options.node_path
        logger.info(f"Complete: {node_path}")
        self.scheduler.run_command_complete(node_path)

        return takler_pb2.ServiceResponse(
            flag=0,
            message="",
        )

    async def RunCommandAbort(self, request: takler_pb2.AbortCommand, context):
        node_path = request.child_options.node_path
        reason = request.reason
        logger.info(f"Abort: {node_path}")
        self.scheduler.run_command_abort(node_path, reason=reason)

        return takler_pb2.ServiceResponse(
            flag=0,
            message="",
        )

    async def RunCommandEvent(self, request, context):
        node_path = request.child_options.node_path
        event_name = request.event_name
        logger.info(f"Event set: {node_path}:{event_name}")
        self.scheduler.run_command_event(node_path, event_name)

        return takler_pb2.ServiceResponse(
            flag=0,
            message="",
        )

    async def RunCommandMeter(self, request: takler_pb2.MeterCommand, context):
        node_path = request.child_options.node_path
        meter = request.meter_name
        value = request.meter_value
        logger.info(f"Meter set: {node_path}:{meter} {value}")
        self.scheduler.run_command_meter(node_path, meter, value)

        return takler_pb2.ServiceResponse(
            flag=0,
            message="",
        )

    # Control command -------------------------------------------------------------

    async def RunCommandRequeue(self, request: takler_pb2.RequeueCommand, context):
        node_path_list = request.node_path
        for node_path in node_path_list:
            logger.info(f"Requeue: {node_path}")
            self.scheduler.run_command_requeue(node_path)

        return takler_pb2.ServiceResponse(
            flag=0,
            message="",
        )

    async def RunCommandSuspend(self, request: takler_pb2.SuspendCommand, context):
        node_paths = request.node_path
        for node_path in node_paths:
            logger.info(f"Suspend: {node_path}")
            self.scheduler.run_command_suspend(node_path)

        return takler_pb2.ServiceResponse(
            flag=0,
            message="",
        )

    async def RunCommandResume(self, request: takler_pb2.SuspendCommand, context):
        node_paths = request.node_path
        for node_path in node_paths:
            logger.info(f"Resume: {node_path}")
            self.scheduler.run_command_resume(node_path)

        return takler_pb2.ServiceResponse(
            flag=0,
            message="",
        )

    async def RunCommandRun(self, request, context):
        node_paths = request.node_path
        force = request.force
        for node_path in node_paths:
            result = self.scheduler.run_command_run(node_path, force=force)
            if result:
                logger.info(f"Run: {node_path}")
            else:
                logger.info(f"Run has error: {node_path}")

        return takler_pb2.ServiceResponse(
            flag=0,
            message="",
        )

    async def RunCommandForce(self, request: takler_pb2.ForceCommand, context):
        paths = request.path
        state = takler_pb2.ForceCommand.ForceState.Name(request.state)
        recursive = request.recursive

        for variable_path in paths:
            result = self.scheduler.run_command_force(variable_path, state=state, recursive=recursive)
            if result:
                logger.info(f"Force: {variable_path} {state}")
            else:
                logger.info(f"Force has error: {variable_path} {state}")

        return takler_pb2.ServiceResponse(
            flag=0,
            message="",
        )

    async def RunCommandFreeDep(self, request: takler_pb2.FreeDepCommand, context):
        paths = request.path
        dep_type = takler_pb2.FreeDepCommand.DepType.Name(request.dep_type)
        for path in paths:
            result = self.scheduler.run_command_free_dep(path, dep_type)
            logger.info(f"Free Dep: {dep_type} {path}")
        return takler_pb2.ServiceResponse(
            flag=0,
            message="",
        )

    async def RunCommandLoad(self, request: takler_pb2.LoadCommand, context):
        flow_type = request.flow_type
        flow_bytes = request.flow
        logger.info(f"Load flow from bytes...")
        self.scheduler.run_command_load(flow_type=flow_type, flow_bytes=flow_bytes)
        return takler_pb2.ServiceResponse(
            flag=0,
            message="",
        )

    # Query command -----------------------------------------------------

    async def RunRequestShow(self, request: takler_pb2.ShowRequest, context):
        output = self.scheduler.handle_request_show(
            show_parameter=request.show_parameter,
            show_trigger=request.show_trigger,
            show_limit=request.show_limit,
            show_event=request.show_event,
            show_meter=request.show_meter,
        )
        return takler_pb2.ShowResponse(
            output=output
        )

    async def RunRequestPing(self, request, context):
        return takler_pb2.PingResponse()

    async def QueryCoroutine(self, request, context):
        loop = asyncio.get_running_loop()
        tasks = []
        for t in asyncio.all_tasks(loop=loop):
            task = takler_pb2.Coroutine(
                name=t.get_name(),
                description=repr(t.get_coro()),
            )
            tasks.append(task)
        return takler_pb2.CoroutineResponse(
            coroutines=tasks
        )

