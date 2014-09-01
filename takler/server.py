import argparse

from takler.constant import DEFAULT_HOST, DEFAULT_PORT
from takler.takler_service import TaklerService
from takler.takler_service.ttypes import *
from takler.service_handler import TaklerServiceHandler

from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
from thrift.server import TServer


class Server(object):
    def __init__(self):
        # server
        self.host = DEFAULT_HOST
        self.port = DEFAULT_PORT
        self.takler_service_handler = TaklerServiceHandler()
        self.thrift_processor = None
        self.thrift_transport = None
        self.thrift_transport_factory = None
        self.thrift_protocol_factory = None
        self.thrift_server = None

    def run_server(self):
        self.takler_service_handler = TaklerServiceHandler()
        self.thrift_processor = TaklerService.Processor(self.takler_service_handler)
        self.thrift_transport = TSocket.TServerSocket(port=self.port)
        self.thrift_transport_factory = TTransport.TBufferedTransportFactory()
        self.thrift_protocol_factory = TBinaryProtocol.TBinaryProtocolFactory()
        self.thrift_server = TServer.TSimpleServer(self.thrift_processor,
                                                   self.thrift_transport,
                                                   self.thrift_transport_factory,
                                                   self.thrift_protocol_factory)
        # You could do one of these for a multithreaded server
        #server = TServer.TThreadedServer(processor, transport, tfactory, pfactory)
        #server = TServer.TThreadPoolServer(processor, transport, tfactory, pfactory)
        print "Starting server at {server_host}:{server_port}".format(
            server_host=self.host,
            server_port=self.port
        )
        self.thrift_server.serve()
        print "Stop server..."


def main():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description="""\
DESCRIPTION
    Run takler server.""")
    parser.add_argument(
        "-p", "--port",
        help="port number")
    args = parser.parse_args()

    server = Server()
    if args.port:
        server.port = args.port
    else:
        print "Using default port: {default_port}".format(default_port=DEFAULT_PORT)
    server.run_server()


if __name__ == "__main__":
    main()