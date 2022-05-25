import asyncio
import time
from io import StringIO
from queue import Queue
from typing import Optional

from takler.core import Bunch, Task, NodeStatus, Event
from takler.core.node import Node
from takler.logging import get_logger
from takler.visitor import pre_order_travel, PrintVisitor


logger = get_logger("server.scheduler")


class Scheduler:
    """
    定时调度器，定时遍历所有 Flow，运行满足依赖条件的任务，同时还负责执行 Flow 操作。

    Attributes
    ----------
    bunch : Bunch
        Scheduler has only one bunch.
    interval_main_loop : float
        time interval to check flow dependencies, unit is seconds.
    """
    def __init__(self, bunch: Bunch):
        self.bunch: Bunch = bunch
        self.interval_main_loop: float = 10.0
        self.command_queue: Queue = Queue()
        self.should_stop: bool = False

    async def start(self):
        pass

    async def run(self):
        """
        Start main loop.
        """
        await self.main_loop()
        await self.shutdown()

    async def shutdown(self):
        """
        Called after main loop is done, unset ``should_stop`` flag.
        """
        self.should_stop = False

    async def main_loop(self):
        """
        Main loop of scheduler.
        """
        while not self.should_stop:
            logger.info("main loop...")
            start_time = time.time()

            self.travel_bunch()

            elapsed = time.time() - start_time
            if elapsed > self.interval_main_loop:
                duration = 0
            else:
                duration = self.interval_main_loop - elapsed

            await asyncio.sleep(duration)

    async def stop(self):
        """
        Stop scheduler and wait until main loop unset ``should_stop`` flag
        """
        logger.info("scheduler shutting down...")
        self.should_stop = True

        while self.should_stop:
            await asyncio.sleep(0.1)
        logger.info("scheduler shutting down...done")

    def travel_bunch(self):
        """
        Travel all flows in bunch to resolve dependencies.

        This function will submit tasks which fit its dependencies.
        """
        for name, flow in self.bunch.flows.items():
            flow.resolve_dependencies()

    # Child -------------------------------------------------

    async def run_command_init(self, node_path: str, task_id: str):
        node = self.bunch.find_node(node_path)
        if node is None:
            raise ValueError(f"node is not found: {node_path}")

        if isinstance(node, Task):
            node.init(task_id)
        else:
            raise ValueError(f"node must be Task: {node_path}")

    def run_command_complete(self, node_path: str):
        node = self.bunch.find_node(node_path)
        if node is None:
            raise ValueError(f"node is not found: {node_path}")

        if isinstance(node, Task):
            node.complete()
        else:
            raise ValueError(f"node must be Task: {node_path}")

    def run_command_abort(self, node_path: str, reason: Optional[str] = None):
        node = self.bunch.find_node(node_path)
        if node is None:
            raise ValueError(f"node is not found: {node_path}")

        if isinstance(node, Task):
            node.abort(reason)
        else:
            raise ValueError(f"node must be Task: {node_path}")

    def run_command_event(self, node_path: str, event_name: str):
        node = self.bunch.find_node(node_path)
        if node is None:
            raise ValueError(f"node is not found: {node_path}")

        node.set_event(event_name, True)

    def run_command_meter(self, node_path: str, meter_name: str, meter_value: str):
        node = self.bunch.find_node(node_path)
        if node is None:
            raise ValueError(f"node is not found: {node_path}")

        node.set_meter(meter_name, int(meter_value))

    # Control -------------------------------------------------

    def run_command_requeue(self, node_path: str):
        node = self.bunch.find_node(node_path)
        if node is None:
            raise ValueError(f"node is not found: {node_path}")

        node.requeue()

    def run_command_suspend(self, node_path: str):
        node = self.bunch.find_node(node_path)
        if node is None:
            raise ValueError(f"node is not found: {node_path}")

        node.suspend()

    def run_command_resume(self, node_path: str):
        node = self.bunch.find_node(node_path)
        if node is None:
            raise ValueError(f"node is not found: {node_path}")

        node.resume()

    def run_command_run(self, node_path: str, force: bool = False) -> bool:
        node = self.bunch.find_node(node_path)
        if not isinstance(node, Task):
            return False
        if not force:
            status = node.state.node_status
            if status in (NodeStatus.submitted, NodeStatus.active):
                # don't run
                return False

        node.run()
        return True

    def run_command_force(self, variable_path: str, state: str, recursive: bool = False) -> bool:
        variable = self.bunch.find_path(variable_path)
        if variable is None:
            return False
        if isinstance(variable, Node):
            # if state in NodeStatus:
            node_status = NodeStatus[state]
            # else:
            #     raise ValueError(f"state {state} is not supported for Node")
            if recursive:
                variable.sink_status_change(node_status)
            else:
                variable.set_node_status(node_status)
            return True
        elif isinstance(variable, Event):
            if state == "set":
                variable.value = True
            elif state == "clear":
                variable.value = False
            else:
                raise ValueError(f"state {state} is not supported for Event")
            return True
        return True

    # Query -------------------------------------------------

    def handle_request_show(self) -> str:
        stream = StringIO()

        for name, flow in self.bunch.flows.items():
            pre_order_travel(flow, PrintVisitor(stream=stream))

        return stream.getvalue()
