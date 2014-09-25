import os


class TaklerScriptFile(object):
    def __init__(self, node, script_path):
        self.node = node
        self.script_path = script_path
        self.job_script_lines = []

    def create_job_script_file(self):
        if not os.path.isfile(self.script_path):
            raise Exception("{script_path} file doesn't exist.".format(script_path=self.script_path))
        with open(self.script_path, 'r') as script_file:
            script_lines = script_file.readlines()
        self.job_script_lines = script_lines
        self.substitute_variable()
        self.write_job_script_file_to_disk()

    def substitute_variable(self):
        for cur_line_index in range(0, len(self.job_script_lines)):
            cur_line = self.job_script_lines[cur_line_index]
            parsed_line = self.node.substitute_variable(cur_line)
            self.job_script_lines[cur_line_index] = parsed_line

    def write_job_script_file_to_disk(self):
        job_file_path = self.node.get_job_path()
        if job_file_path is None:
            raise Exception("can't generate job_file_path")
        dir_name = os.path.dirname(job_file_path)
        if not os.path.isdir(dir_name):
            os.makedirs(dir_name)

        with open(job_file_path, 'w') as job_file:
            job_file.writelines(self.job_script_lines)