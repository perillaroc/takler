from takler.takler_service.ttypes import *
from takler.node import Node
from takler.logger import server_logger


class TaklerServiceHandler:
    def __init__(self, bunch):
        self.bunch = bunch
        self.logger = server_logger

    def queue(self, node_path):
        """
        Parameters:
         - node_path
        """
        self.logger.info("[TaklerServiceHandler] Queue {node_path}".format(node_path=node_path))
        some_node = self.bunch.find_node(node_path)
        some_node.queue()
        return ServiceResponse(0, "ok")

    def run(self, node_path):
        """
        Parameters:
         - node_path
        """
        self.logger.info("[TaklerServiceHandler] Submit {node_path}".format(node_path=node_path))
        some_node = self.bunch.find_node(node_path)
        some_node.run()
        return ServiceResponse(0, "ok")

    def init(self, node_path, task_id):
        """
        Parameters:
         - node_path
         - node_rid
        """
        self.logger.info("[TaklerServiceHandler] Init {node_path} with node id {task_id}"
                    .format(node_path=node_path,task_id=task_id))
        some_node = self.bunch.find_node(node_path)
        some_node.init(task_id)
        return ServiceResponse(0, "ok")

    def complete(self, node_path):
        """
        Parameters:
         - node_path
        """
        self.logger.info("[TaklerServiceHandler] Complete {node_path}".format(node_path=node_path))
        some_node = self.bunch.find_node(node_path)
        some_node.complete()
        return ServiceResponse(0, "ok")

    def abort(self, node_path):
        """
        Parameters:
         - node_path
        """
        self.logger.info("[TaklerServiceHandler] Abort {node_path}".format(node_path=node_path))
        some_node = self.bunch.find_node(node_path)
        some_node.abort()
        return ServiceResponse(0, "ok")

    def kill(self, node_path):
        """
        Parameters:
         - node_path
        """
        self.logger.info("[TaklerServiceHandler] Kill {node_path}".format(node_path=node_path))
        some_node = self.bunch.find_node(node_path)
        some_node.kill()
        return ServiceResponse(0, "ok")

    def bunch_tree(self):
        self.logger.info("[TaklerServiceHandler] Get bunch tree")
        ret = self.bunch.to_json()
        return ServiceResponse(0, ret)

    def add_suite(self, suite_json_str):
        """
        Parameters:
         - suite_json_str
        """
        self.logger.info("[TaklerServiceHandler] add suite")
        a_new_suite = Node.create_from_json(suite_json_str)
        if self.bunch.find_suite(a_new_suite.name) is None:
            self.bunch.add_suite(a_new_suite)
        else:
            raise InvalidRequestException(
                why="Suite is already exists.")
        return ServiceResponse(0, "ok")

    def update_suite(self, suite_json_str):
        """
        Parameters:
         - suite_json_str
        """
        a_suite = Node.create_from_json(suite_json_str)
        self.logger.info("[TaklerServiceHandler] update suite {suite_name}".format(suite_name=a_suite.name))
        if self.bunch.find_suite(a_suite.name) is None:
            raise InvalidRequestException(
                why="Suite doesn't exists.")
        self.bunch.update_suite(a_suite)
        return ServiceResponse(0, "ok")

    def update_node(self, node_path, node_json_str):
        """
        :param node_path:
        :param node_json_str:
        :return: ServiceResponse
        """
        self.logger.info("[TaklerServiceHandler] update node {node_path}".format(node_path=node_path))
        node = Node.create_from_json(node_json_str)
        try:
            self.bunch.update_node(node_path, node)
        except Exception, exp:
            raise InvalidRequestException(why=exp.message)
        return ServiceResponse(0, "ok")