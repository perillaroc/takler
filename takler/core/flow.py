from typing import TYPE_CHECKING, Optional

from .node_container import NodeContainer
from .parameter import Parameter

if TYPE_CHECKING:
    from .bunch import Bunch


class Flow(NodeContainer):
    def __init__(self, name: str):
        super(Flow, self).__init__(name)

        self.bunch = None  # type: Optional[Bunch]

    # Node access --------------------------------------

    def get_bunch(self):  # type: () -> Optional[Bunch]
        return self.bunch

    # Parameter ----------------------------------------

    def find_parent_parameter(self, name: str) -> Optional[Parameter]:
        p = super(Flow, self).find_parent_parameter(name)
        if p is not None:
            return p

        if self.bunch is None:
            return None

        return self.bunch.find_parent_parameter(name)
