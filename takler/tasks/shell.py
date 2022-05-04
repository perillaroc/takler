from typing import Union, Optional, Dict
from pathlib import Path

from pydantic import BaseModel

from takler.core import Task, Parameter
from takler.core.parameter import TAKLER_HOME


# Task level
TAKLER_SCRIPT = "TAKLER_SCRIPT"
TAKLER_JOB = "TAKLER_JOB"
TAKLER_JOBOUT = "TAKLER_JOBOUT"

# Script
SCRIPT_EXTENSION = "takler"
JOB_SCRIPT_EXTENSION = "job"
JOB_OUTPUT_EXTENSION = "out"
JOB_OUTPUT_ERROR_EXTENSION = "err"


class ShellScriptTask(Task):
    def __init__(self, name: str, script_path: Union[str, Path]):
        super(ShellScriptTask, self).__init__(name)

        self.script_path = script_path

        self.shell_generated_parameters = ShellScriptTaskGeneratedParameters(node=self)

    # Parameter -------------------------------------------------

    def update_generated_parameters(self):
        self.shell_generated_parameters.update_parameters()
        super(ShellScriptTask, self).update_generated_parameters()

    def find_generated_parameter(self, name: str) -> Optional[Parameter]:
        p = self.shell_generated_parameters.find_parameter(name)
        if p is not None:
            return p

        p = super(ShellScriptTask, self).find_generated_parameter(name)
        return p

    def generated_parameters_only(self) -> Dict[str, Parameter]:
        task_params = super(ShellScriptTask, self).generated_parameters_only()
        params = self.shell_generated_parameters.generate_variables()
        for key, p in task_params.items():
            if key not in params:
                params[key] = p
        return params

    # Operation -------------------------------------------------

    def run(self):
        """
        run shell command
        """

    def submit(self):
        """
        Submit shell script to background.
        """
        pass


class ShellScriptTaskGeneratedParameters(BaseModel):
    node: ShellScriptTask
    takler_script: Parameter = Parameter(TAKLER_SCRIPT, None)
    takler_job: Parameter = Parameter(TAKLER_JOB, None)
    takler_jobout: Parameter = Parameter(TAKLER_JOBOUT, None)

    class Config:
        arbitrary_types_allowed = True

    def update_parameters(self):
        self.takler_script.value = self.node.script_path

        home_param = self.node.find_parent_parameter(TAKLER_HOME)
        job_path = Path(f"{home_param.value}{self.node.node_path}.{JOB_SCRIPT_EXTENSION}")
        self.takler_job.value = job_path.absolute()

        jobout_path = Path(f"{home_param.value}{self.node.node_path}.{JOB_OUTPUT_EXTENSION}")
        self.takler_jobout.value = jobout_path.absolute()

    def find_parameter(self, name: str) -> Optional[Parameter]:
        if name == TAKLER_SCRIPT:
            return self.takler_script
        elif name == TAKLER_JOB:
            return self.takler_job
        elif name == TAKLER_JOBOUT:
            return self.takler_jobout
        else:
            return None

    def generate_variables(self) -> Dict[str, Parameter]:
        return {
            TAKLER_SCRIPT: self.takler_script,
            TAKLER_JOB: self.takler_job,
            TAKLER_JOBOUT: self.takler_jobout,
        }
