from takler.takler_service import TaklerService
from takler.takler_service.ttypes import *

from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
from thrift.server import TServer


class TaklerServiceHandler:
    def __init__(self):
        pass

    def init(self, node_path, node_rid):
        """
        Parameters:
         - node_path
         - node_rid
        """
        print "init {node_path} with pid {node_rid}".format(
            node_path=node_path,
            node_rid=node_rid
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

handler = TaklerServiceHandler()
processor = TaklerService.Processor(handler)
transport = TSocket.TServerSocket(port=88705)
tfactory = TTransport.TBufferedTransportFactory()
pfactory = TBinaryProtocol.TBinaryProtocolFactory()

server = TServer.TSimpleServer(processor, transport, tfactory, pfactory)

# You could do one of these for a multithreaded server
#server = TServer.TThreadedServer(processor, transport, tfactory, pfactory)
#server = TServer.TThreadPoolServer(processor, transport, tfactory, pfactory)

print 'Starting the server...'
server.serve()
print 'done.'