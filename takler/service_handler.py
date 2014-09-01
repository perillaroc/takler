from takler.takler_service.ttypes import *


class TaklerServiceHandler:
    def __init__(self):
        pass

    def init(self, node_path, node_id):
        """
        Parameters:
         - node_path
         - node_rid
        """
        print "init {node_path} with node id {node_id}".format(
            node_path=node_path,
            node_id=node_id
        )
        return ServiceResponse(0, "ok")

    def complete(self, node_path):
        """
        Parameters:
         - node_path
        """
        print "complete"
        return ServiceResponse(0, "ok")

    def abort(self, node_path):
        """
        Parameters:
         - node_path
        """
        print "abort"
        return ServiceResponse(0, "ok")