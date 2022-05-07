# from takler.visitor import pre_order_travel, SimplePrintVisitor
from takler.tasks import ShellScriptTask


def test_generated_parameters(shell_task_bunch):
    flow1 = shell_task_bunch.flow1
    # pre_order_travel(flow1, SimplePrintVisitor())

    task1 = shell_task_bunch.task1  # type: ShellScriptTask
    task1.update_generated_parameters()
    params = task1.parameters()
    for key, p in params.items():
        print(key, p.value)
