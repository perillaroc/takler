import functools
import asyncio
from typing import Optional, Dict

from pydantic import BaseModel

from .node import Node
from .state import NodeStatus
from .parameter import (
    Parameter,
    TASK, TAKLER_NAME, TAKLER_RID
)
from ._logger import logger


class Task(Node):
    def __init__(self, name: str):
        super(Task, self).__init__(name)
        self.task_id: Optional[str] = None

        self.aborted_reason: Optional[str] = None

        self.generated_parameters: TaskNodeGeneratedParameters = TaskNodeGeneratedParameters(node=self)

    def __repr__(self):
        return f"Task {self.name}"

    # State management --------------------------------------------

    def computed_status(self, immediate: bool) -> NodeStatus:
        """
        The status of a task is its own status.
        """
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

        # don't run when task is aborted. See :github:issue:`27`
        if node_status == NodeStatus.aborted:
            return False

        # run jobs
        self.run()

        return True

    # Parameter ---------------------------------------------------

    def find_generated_parameter(self, name: str) -> Optional[Parameter]:
        return self.generated_parameters.find_parameter(name)

    def update_generated_parameters(self):
        self.generated_parameters.update_parameters()

    def generated_parameters_only(self) -> Dict[str, Parameter]:
        return self.generated_parameters.generated_parameters()

    # Node Operation ----------------------------------------------
    #   Node operation is used to control the flow.

    def run(self):
        """
        Run the task, set status to ``NodeStatus.submitted`` and handle status change.

        Subclasses of ``Task`` should reimplement this method to do the real run operation and deal with errors.
        """
        # change node status
        self.set_node_status(node_status=NodeStatus.submitted)
        self.aborted_reason = None
        logger.info(f"run: {self.node_path}")
        self.handle_status_change()

    def requeue(self):
        self.aborted_reason = None
        super(Task, self).requeue()

    # Status update operation -------------------------------------
    #   Status update operation is used in task's running period,
    #   in order to notify task's status change to takler server.

    def init(self, task_id: str = ""):
        self.task_id = task_id
        self.set_node_status(node_status=NodeStatus.active)
        logger.info(f"init: {self.node_path}")
        self.handle_status_change()

    def complete(self):
        self.set_node_status(node_status=NodeStatus.complete)
        logger.info(f"complete: {self.node_path}")
        self.handle_status_change()

    def abort(self, reason: str = ""):
        self.set_node_status(node_status=NodeStatus.aborted)
        self.aborted_reason = reason
        logger.info(f"abort: {self.node_path} {reason}")
        self.handle_status_change()


class TaskNodeGeneratedParameters(BaseModel):
    node: Task
    task: Parameter = Parameter(TASK, None)
    takler_name: Parameter = Parameter(TAKLER_NAME, None)
    takler_rid: Parameter = Parameter(TAKLER_RID, None)

    class Config:
        arbitrary_types_allowed = True

    def update_parameters(self):
        """
        Update generated parameters from task node's attrs.
        """
        self.task.value = self.node.name
        self.takler_name.value = self.node.node_path
        self.takler_rid.value = self.node.task_id

    def find_parameter(self, name: str) -> Optional[Parameter]:
        if name == TASK:
            return self.task
        elif name == TAKLER_NAME:
            return self.takler_name
        elif name == TAKLER_RID:
            return self.takler_rid
        else:
            return None

    def generated_parameters(self) -> Dict[str, Parameter]:
        return {
            TASK: self.task,
            TAKLER_NAME: self.takler_name,
            TAKLER_RID: self.takler_rid
        }


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
                    kwargs.update(self=self)
                    func(*args, **kwargs)
                    self.complete()

            return RunTask()
        return wrapper
    return decorator


def async_task(name: str):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            class RunTask(Task):
                def __init__(self):
                    super(RunTask, self).__init__(name=name)

                async def run(self):
                    Task.run(self)

                    async def run_func():
                        kwargs.update(self=self)
                        self.init()
                        await func(*args, **kwargs)
                        self.complete()

                    asyncio.run(run_func())

            return RunTask()
        return wrapper
    return decorator

