from takler.core import Task


class ShellTask(Task):
    def __init__(self, name: str):
        super(ShellTask, self).__init__(name)

    def run(self):
        """
        run shell command
        """
