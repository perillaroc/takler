from typing import Optional, Union, List
from datetime import datetime

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

    def set_host_port(self, host: str, port: Union[int, str]):
        self.host = host
        self.port = str(port)

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

    def init(self, node_path: str, task_id: str):
        self.start()
        self.run_command_init(node_path=node_path, task_id=task_id)
        self.shutdown()

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

    def complete(self, node_path: str):
        self.start()
        self.run_command_complete(node_path=node_path)
        self.shutdown()

    def run_command_complete(self, node_path: str):
        response = self.stub.RunCompleteCommand(
            takler_pb2.CompleteCommand(
                child_options=takler_pb2.ChildCommandOptions(
                    node_path=node_path,
                )
            )
        )
        print(f"received: {response.flag}")

    def abort(self, node_path: str, reason: str):
        self.start()
        self.run_command_abort(node_path=node_path, reason=reason)
        self.shutdown()

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

    def event(self, node_path: str, event_name: str):
        self.start()
        self.run_command_event(node_path=node_path, event_name=event_name)
        self.shutdown()

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

    def meter(self, node_path: str, meter_name: str, meter_value: str):
        self.start()
        self.run_command_meter(node_path=node_path, meter_name=meter_name, meter_value=meter_value)
        self.shutdown()

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

    def requeue(self, node_path: List[str]):
        self.start()
        self.run_command_requeue(node_path=node_path)
        self.shutdown()

    def run_command_requeue(self, node_path: List[str]):
        response = self.stub.RunRequeueCommand(
            takler_pb2.RequeueCommand(
                node_path=node_path
            )
        )
        print(f"received: {response.flag}")

    def suspend(self, node_path: List[str]):
        self.start()
        self.run_command_suspend(node_path=node_path)
        self.shutdown()

    def run_command_suspend(self, node_path: List[str]):
        response = self.stub.RunSuspendCommand(
            takler_pb2.SuspendCommand(
                node_path=node_path
            )
        )
        print(f"received: {response.flag}")

    def resume(self, node_path: List[str]):
        self.start()
        self.run_command_resume(node_path=node_path)
        self.shutdown()

    def run_command_resume(self, node_path: List[str]):
        response = self.stub.RunResumeCommand(
            takler_pb2.SuspendCommand(
                node_path=node_path
            )
        )
        print(f"received: {response.flag}")

    def run(self, node_path: List[str], force: bool):
        self.start()
        self.run_command_run(node_path=node_path, force=force)
        self.shutdown()

    def run_command_run(self, node_path: List[str], force: bool):
        response = self.stub.RunRunCommand(
            takler_pb2.RunCommand(
                force=force,
                node_path=node_path
            )
        )
        print(f"received: {response.flag}")

    def force(self, variable_paths: List[str], state: str, recursive: bool):
        self.start()
        self.run_command_force(variable_paths=variable_paths, state=state, recursive=recursive)
        self.shutdown()

    def run_command_force(self, variable_paths: List[str], state: str, recursive: bool):
        response = self.stub.RunForceCommand(
            takler_pb2.ForceCommand(
                state=takler_pb2.ForceCommand.ForceState.Value(state),
                recursive=recursive,
                path=variable_paths,
            )
        )
        print(f"received: {response.flag}")

    # Query command ----------------------------------------------------

    def show(
            self,
            show_parameter: bool = False,
            show_trigger: bool = True,
            show_limit: bool = True,
            show_event: bool = True,
            show_meter: bool = True,
    ):
        self.start()
        self.run_request_show(
            show_trigger=show_trigger,
            show_parameter=show_parameter,
            show_limit=show_limit,
            show_event=show_event,
            show_meter=show_meter,
        )
        self.shutdown()

    def run_request_show(
            self,
            show_trigger: bool,
            show_parameter: bool,
            show_limit: bool,
            show_event: bool,
            show_meter: bool
    ):
        response = self.stub.RunShowRequest(
            takler_pb2.ShowRequest(
                show_trigger=show_trigger,
                show_parameter=show_parameter,
                show_limit=show_limit,
                show_event=show_event,
                show_meter=show_meter,
            )
        )
        print(response.output)

    def ping(self):
        start_time = datetime.now()
        self.start()
        self.run_request_ping()
        end_time = datetime.now()
        print(f"ping server ({self.host}:{self.port}) succeeded in {end_time - start_time}.")
        self.shutdown()

    def run_request_ping(self):
        response = self.stub.RunPingRequest(
            takler_pb2.PingResponse()
        )
