from typing import Optional, Dict, Union, List

from pydantic import BaseModel, validator

from takler import constant

from .node_container import NodeContainer
from .flow import Flow
from .node import Node
from .parameter import (
    Parameter, TAKLER_HOST, TAKLER_PORT, TAKLER_HOME
)


class Bunch(NodeContainer):
    def __init__(self, name: str = "", port: str = None):
        super(Bunch, self).__init__(name=name)
        self.flows = dict()  # type: Dict[str, Flow]
        self.server_state = ServerState(port=port)  # type: ServerState
        self.server_state.setup()

    # Flow ------------------------------------------------

    def add_flow(self, flow: Union[Flow, str]) -> Flow:
        if isinstance(flow, str):
            flow = Flow(name=flow)
        self.flows[flow.name] = flow
        flow.bunch = self
        return flow

    def find_flow(self, name: str) -> Optional[Flow]:
        return self.flows.get(name, None)

    def delete_flow(self, flow: Union[str, Flow]) -> Flow:
        if isinstance(flow, Flow):
            flow_name = flow.name
        else:
            flow_name = flow

        if flow_name not in self.flows:
            raise ValueError(f"flow is not in Bunch: {flow_name}")

        flow = self.flows.pop(flow_name)

        return flow

    # Node access -----------------------------------------------

    def find_node(self, a_path: str) -> Optional[Node]:
        if not Node.check_absolute_node_path(a_path):
            raise ValueError(f"absolute node path is illegal: {a_path}")
        tokens = a_path.split("/")
        assert len(tokens) > 1
        flow_name = tokens[1]
        a_flow = self.find_flow(flow_name)
        if a_flow is None:
            return None
        return a_flow.find_node(a_path)

    # Parameter ------------------------------------------------

    def find_generated_parameter(self, name: str) -> Optional[Parameter]:
        p = self.server_state.find_parameter(name)
        return p

    def generated_parameters_only(self) -> Dict[str, Parameter]:
        return self.server_state.generated_parameters()


class ServerState(BaseModel):
    server_parameters: List[Parameter] = []
    host: str = constant.DEFAULT_HOST
    port: Optional[str] = constant.DEFAULT_PORT

    class Config:
        arbitrary_types_allowed = True
        validate_assignment = True

    @validator("port")
    def set_port(cls, p):
        if p is None:
            p = constant.DEFAULT_PORT
        return p

    def setup(self):
        self.setup_default_server_parameters()

    def setup_default_server_parameters(self):
        self.server_parameters.append(Parameter(TAKLER_HOST, self.host))
        self.server_parameters.append(Parameter(TAKLER_PORT, self.port))
        self.server_parameters.append(Parameter(TAKLER_HOME, "."))

    def find_parameter(self, name: str) -> Optional[Parameter]:
        for p in self.server_parameters:
            if p.name == name:
                return p

        return None

    def generated_parameters(self) -> Dict[str, Parameter]:
        params = dict()
        for p in self.server_parameters:
            params[p.name] = p
        return params
