import os
import sys


class ShellRunner:
    def spwan(self, command: str):
        """
        Double fork to run shell command `command` to avoid zombie process.

        The command will be run as follows:

            /bin/sh -c command_string
        """
        try:
            pid = os.fork()
            if pid > 0:
                # parent process, return and keep running
                return
        except OSError:
            pass

        os.setsid()

        # do second fork
        try:
            pid = os.fork()
            if pid > 0:
                # exit from second parent
                sys.exit(0)
        except OSError:
            pass

        os.execl("/bin/sh", "sh", "-c", command)

        os._exit(127)
