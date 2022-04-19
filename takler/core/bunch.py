from typing import Optional, Dict, Union

from .node_container import NodeContainer
from .flow import Flow
from .node import Node


class Bunch(NodeContainer):
    def __init__(self, name: str = ""):
        super(Bunch, self).__init__(name=name)
        self.flows = dict()  # type: Dict[str, Flow]

    def add_flow(self, flow: Union[Flow, str]) -> Flow:
        if isinstance(flow, str):
            flow = Flow(name=flow)
        self.flows[flow.name] = flow
        self.append_child(flow)
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
        self.children.remove(flow)

        return flow

    def find_node(self, node_path: str) -> Optional[Node]:
        if not Node.check_absolute_node_path(node_path):
            raise ValueError(f"absolute node path is illegal: {node_path}")
        tokens = node_path.split("/")
        assert len(tokens) > 1
        flow_name = tokens[1]
        a_flow = self.find_flow(flow_name)
        if a_flow is None:
            return None
        return a_flow.find_node(node_path)
