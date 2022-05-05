from typing import Union
from pathlib import Path

from jinja2 import FileSystemLoader, Environment

from .shell_script_task import ShellScriptTask, TAKLER_JOB


class ShellScript(object):
    def __init__(self, script_path: Union[str, Path], node: ShellScriptTask):
        self.script_path = Path(script_path)
        self.node = node

    def render(self):
        loader_paths = [self.script_path.parent]
        include_param = self.node.find_parameter("TAKLER_INCLUDE")
        if include_param is not None:
            loader_paths.append(include_param.value)
        file_loader = FileSystemLoader(loader_paths)
        env = Environment(loader=file_loader)

        template = env.get_template(self.script_path.name)

        params = self.node.parameters()
        template_params = {key: p.value for key, p in params.items()}
        # print(template_params)

        job_script_content = template.render(**template_params)

        job_script_path = Path(self.node.find_parameter(TAKLER_JOB).value)
        job_script_path.parent.mkdir(parents=True, exist_ok=True)
        with open(job_script_path, "w") as f:
            f.write(job_script_content)
