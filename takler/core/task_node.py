import functools

from .node import Node
from .state import NodeStatus


class Task(Node):
    def __init__(self, name: str):
        super(Task, self).__init__(name)

    def __repr__(self):
        return f"Task {self.name}"

    # State management --------------------------------------------

    def computed_status(self, immediate: bool) -> NodeStatus:
        return self.state.node_status

    def swim_status_change(self):
        """
        Task node use its own status, and needn't compute status again.
        So swim status change from its parent.
        """
        return self.parent.swim_status_change()

    # Trigger -----------------------------------------------------

    def resolve_dependencies(self) -> bool:
        # check node status
        node_status = self.state.node_status
        if node_status in (
            NodeStatus.complete,
            NodeStatus.active,
            NodeStatus.submitted,
            NodeStatus.unknown,
        ):
            return False

        # resolve node dependencies
        if not Node.resolve_dependencies(self):
            return False

        # submit jobs
        self.run()
        return True

    # Node Operation ----------------------------------------------
    #   Node operation is used to control the flow.

    def run(self):
        # TODO: Run task.

        # change node status
        self.set_node_status(node_status=NodeStatus.submitted)
        self.handle_status_change()

    # Status update operation -------------------------------------
    #   Status update operation is used in task's running period,
    #   in order to notify task's status change to takler server.

    def init(self):
        self.set_node_status(node_status=NodeStatus.active)
        self.handle_status_change()

    def complete(self):
        self.set_node_status(node_status=NodeStatus.complete)
        self.handle_status_change()

    def abort(self):
        self.set_node_status(node_status=NodeStatus.aborted)
        self.handle_status_change()


def task(name: str):
    """
    Decorator to create inline task.

    Parameters
    ----------
    name
        task name
    Returns
    -------

    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            class RunTask(Task):
                def __init__(self):
                    super(RunTask, self).__init__(name=name)

                def run(self):
                    Task.run(self)

                    self.init()
                    func(*args, **kwargs)
                    self.complete()

            return RunTask()
        return wrapper
    return decorator


