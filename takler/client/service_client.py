from typing import Optional, Union, List

import grpc

from takler.server.protocol.takler_pb2_grpc import TaklerServerStub
from takler.server.protocol import takler_pb2
from takler.logging import get_logger
from takler.constant import DEFAULT_HOST, DEFAULT_PORT


logger = get_logger("client")


class TaklerServiceClient:
    """
    Notes
    -----
    If HPC login node's name is used, should set an environment to use native DNS resolver.

        export GRPC_DNS_RESOLVER=native

    Or use GOLANG version client.
    """
    def __init__(self, host: str = DEFAULT_HOST, port: Union[int, str] = DEFAULT_PORT):
        self.host: str = host
        self.port: str = str(port)
        self.channel: Optional[grpc.Channel] = None
        self.stub: Optional[TaklerServerStub] = None

    @property
    def listen_address(self) -> str:
        """
        str: gRPC server's listen address
        """
        return f'{self.host}:{self.port}'

    def create_channel(self):
        self.channel = grpc.insecure_channel(self.listen_address)

    def close_channel(self):
        self.channel.close()
        self.channel = None

    def create_stub(self):
        self.stub = TaklerServerStub(self.channel)
        return self.stub

    def start(self):
        self.create_channel()
        self.create_stub()

    def shutdown(self):
        self.close_channel()

    # Child command -------------------------------------------------

    def run_command_init(self, node_path: str, task_id: str):
        response = self.stub.RunInitCommand(
            takler_pb2.InitCommand(
                child_options=takler_pb2.ChildCommandOptions(
                    node_path=node_path,
                ),
                task_id=task_id
            )
        )
        print(f"received: {response.flag}")

    def run_command_complete(self, node_path: str):
        response = self.stub.RunCompleteCommand(
            takler_pb2.CompleteCommand(
                child_options=takler_pb2.ChildCommandOptions(
                    node_path=node_path,
                )
            )
        )
        print(f"received: {response.flag}")

    def run_command_abort(self, node_path: str, reason: str):
        response = self.stub.RunAbortCommand(
            takler_pb2.AbortCommand(
                child_options=takler_pb2.ChildCommandOptions(
                    node_path=node_path,
                ),
                reason=reason
            )
        )
        print(f"received: {response.flag}")

    def run_command_event(self, node_path: str, event_name: str):
        response = self.stub.RunEventCommand(
            takler_pb2.EventCommand(
                child_options=takler_pb2.ChildCommandOptions(
                    node_path=node_path,
                ),
                event_name=event_name,
            )
        )
        print(f"received: {response.flag}")

    def run_command_meter(self, node_path: str, meter_name: str, meter_value: str):
        response = self.stub.RunMeterCommand(
            takler_pb2.MeterCommand(
                child_options=takler_pb2.ChildCommandOptions(
                    node_path=node_path,
                ),
                meter_name=meter_name,
                meter_value=meter_value,
            )
        )
        print(f"received: {response.flag}")

    # Control command ----------------------------------------------------

    def run_command_requeue(self, node_path: str):
        response = self.stub.RunRequeueCommand(
            takler_pb2.RequeueCommand(
                node_path=node_path
            )
        )
        print(f"received: {response.flag}")

    def run_command_suspend(self, node_path: List[str]):
        response = self.stub.RunSuspendCommand(
            takler_pb2.SuspendCommand(
                node_path=node_path
            )
        )
        print(f"received: {response.flag}")

    def run_command_resume(self, node_path: List[str]):
        response = self.stub.RunResumeCommand(
            takler_pb2.SuspendCommand(
                node_path=node_path
            )
        )
        print(f"received: {response.flag}")

    def run_command_run(self, node_path: List[str], force: bool):
        response = self.stub.RunRunCommand(
            takler_pb2.RunCommand(
                force=force,
                node_path=node_path
            )
        )
        print(f"received: {response.flag}")

    # Show command ----------------------------------------------------

    def run_request_show(self):
        response = self.stub.RunShowRequest(
            takler_pb2.ShowRequest()
        )
        print(response.output)
