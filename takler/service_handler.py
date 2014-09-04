from takler.takler_service.ttypes import *


class TaklerServiceHandler:
    def __init__(self, bunch):
        self.bunch = bunch

    def queue(self, node_path):
        """
        Parameters:
         - node_path
        """
        print "[Server] [Queue] {node_path}".format(node_path=node_path)
        some_node = self.bunch.find_node_by_absolute_path(node_path)
        some_node.queue()
        return ServiceResponse(0, "ok")

    def run(self, node_path):
        """
        Parameters:
         - node_path
        """
        print "[Server] [Submit] {node_path}".format(node_path=node_path)
        some_node = self.bunch.find_node_by_absolute_path(node_path)
        some_node.run()
        return ServiceResponse(0, "ok")

    def init(self, node_path, task_id):
        """
        Parameters:
         - node_path
         - node_rid
        """
        print "[Server] [Submit] {node_path} with node id {task_id}".format(node_path=node_path,task_id=task_id)
        some_node = self.bunch.find_node_by_absolute_path(node_path)
        some_node.init(task_id)
        return ServiceResponse(0, "ok")

    def complete(self, node_path):
        """
        Parameters:
         - node_path
        """
        print "[Server] [Complete] {node_path}".format(node_path=node_path)
        some_node = self.bunch.find_node_by_absolute_path(node_path)
        some_node.complete()
        return ServiceResponse(0, "ok")

    def abort(self, node_path):
        """
        Parameters:
         - node_path
        """
        print "[Server] [Abort] {node_path}".format(node_path=node_path)
        some_node = self.bunch.find_node_by_absolute_path(node_path)
        some_node.abort()
        return ServiceResponse(0, "ok")

    def kill(self, node_path):
        """
        Parameters:
         - node_path
        """
        print "[Server] [Kill] {node_path}".format(node_path=node_path)
        some_node = self.bunch.find_node_by_absolute_path(node_path)
        some_node.kill()
        return ServiceResponse(0, "ok")