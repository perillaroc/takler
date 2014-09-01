from takler.constant import DEFAULT_HOST, DEFAULT_PORT
from takler.takler_service import TaklerService
from takler.takler_service.ttypes import *

from thrift import Thrift
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol


class Client(object):
    def __init__(self):
        self.host = DEFAULT_HOST
        self.port = DEFAULT_PORT
        self.path = "/"
        self.pid = ""

    def queue(self, node_path):
        pass

    def run(self, node_path, node_rid):
        # Make socket
        transport = TSocket.TSocket(self.host, self.port)

        # Buffering is critical. Raw sockets are very slow
        transport = TTransport.TBufferedTransport(transport)

        # Wrap in a protocol
        protocol = TBinaryProtocol.TBinaryProtocol(transport)

        # Create a client to use the protocol encoder
        takler_client = TaklerService.Client(protocol)

        # Connect!
        transport.open()

        server_response = takler_client.init(node_path, node_rid)
        print server_response

        # Close!
        transport.close()

    def init(self, node_path, pid):
        self.pid = pid

    def complete(self, node_path):
        pass

    def aborted(self, node_path):
        pass

if __name__ == "__main__":
    client = Client()
    client.run("/suite1/family1/task1", "1234567")