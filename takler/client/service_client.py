from typing import Optional

import grpc

from takler.server.protocol.takler_pb2_grpc import TaklerServerStub
from takler.server.protocol import takler_pb2
from takler.logging import get_logger


logger = get_logger("client")


class TaklerServiceClient:
    def __init__(self, host: str = "localhost", port: int = 33083):
        self.host: str = host
        self.port: int = port
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

    def run_command_requeue(self, node_path: str):
        response = self.stub.RunRequeueCommand(
            takler_pb2.RequeueCommand(
                node_path=node_path
            )
        )
        print(f"received: {response.flag}")

    def run_request_show(self):
        response = self.stub.RunShowRequest(
            takler_pb2.ShowRequest()
        )
        print(response.output)
