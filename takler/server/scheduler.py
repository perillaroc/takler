import asyncio
import time
from io import StringIO
from typing import Optional, Union
from queue import Queue, Empty


from takler.core import Bunch, Task
from takler.core.node import Node
from takler.logging import get_logger
from takler.visitor import NodeVisitor, pre_order_travel


logger = get_logger("server.scheduler")


class Scheduler:
    def __init__(self, bunch: Bunch):
        self.bunch = bunch  # type: Bunch
        self.interval_main_loop = 10.0  # type: float
        self.command_queue = Queue()  # type: Queue

    async def start(self):
        pass

    async def run(self):
        await self.main_loop()

    async def main_loop(self):
        while True:
            logger.info("main loop...")
            start_time = time.time()

            self.travel_bunch()

            elapsed = time.time() - start_time
            if elapsed > self.interval_main_loop:
                duration = 0
            else:
                duration = self.interval_main_loop - elapsed

            await asyncio.sleep(duration)

    def travel_bunch(self):
        for name, flow in self.bunch.flows.items():
            flow.resolve_dependencies()

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

    def run_command_abort(self, node_path: str):
        node = self.bunch.find_node(node_path)
        if node is None:
            raise ValueError(f"node is not found: {node_path}")

        if isinstance(node, Task):
            node.abort()
        else:
            raise ValueError(f"node must be Task: {node_path}")

    def handle_show_request(self) -> str:
        stream = StringIO()

        class PrintVisitor(NodeVisitor):
            def __init__(self):
                NodeVisitor.__init__(self)
                self.level = 0

            def visit(self, node: Node):
                place_holder = "  " * self.level
                node_name = node.name
                node_state = node.state.node_status.name
                stream.write(f"{place_holder}|- {node_name} [{node_state}]\n")

            def before_visit_child(self):
                self.level += 1

            def after_visit_child(self):
                self.level -= 1

        for name, flow in self.bunch.flows.items():
            pre_order_travel(flow, PrintVisitor())

        return stream.getvalue()
