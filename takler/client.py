import argparse
import json
from takler.constant import DEFAULT_HOST, DEFAULT_PORT
from takler.takler_service import TaklerService
from takler.takler_service.ttypes import *
from takler.logger import client_logger

from thrift import Thrift
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol


class Client(object):
    def __init__(self):
        self.host = DEFAULT_HOST
        self.port = DEFAULT_PORT
        self.path = "/"
        self.node_id = ""
        self.logger_name = 'takler-client'
        self.logger = client_logger

    def run_command(self, command, *args):
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

        command_mapper = {
            "queue": takler_client.queue,
            "run": takler_client.run,
            "init": takler_client.init,
            "complete": takler_client.complete,
            "abort": takler_client.abort,
            "kill": takler_client.kill,
            "bunch_tree": takler_client.bunch_tree,
            "add_suite": takler_client.add_suite,
            "update_suite": takler_client.update_suite,
            "update_node": takler_client.update_node
        }
        server_response = None
        if command in command_mapper:
            try:
                server_response = command_mapper[command](*args)
                self.logger.info("[{name}]{server_response}".format(name="Client", server_response=server_response))
            except InvalidRequestException, e:
                self.logger.exception("[Client]got exception: {why}".format(why=e.why))
                transport.close()
                raise
        else:
            self.logger.info("command is not right: {command}".format(command=command))

        # Close!
        transport.close()
        return server_response

    def queue(self, node_path):
        return self.run_command("queue", node_path)

    def run(self, node_path):
        return self.run_command("run", node_path)

    def init(self, node_path, node_id):
        self.node_id = node_id
        return self.run_command("init", node_path, node_id)

    def complete(self, node_path):
        return self.run_command("complete", node_path)

    def abort(self, node_path):
        return self.run_command("abort", node_path)

    def kill(self, node_path):
        return self.run_command("kill", node_path)

    def get_bunch_tree(self):
        server_response = self.run_command("bunch_tree")
        return json.loads(server_response.str)

    def get_bunch_tree_str(self):
        return json.dumps(self.get_bunch_tree(), indent=4, separators=(',', ':'))

    def add_suite(self, suite):
        return self.run_command("add_suite", suite.to_json())

    def update_suite(self, suite):
        return self.run_command("update_suite", suite.to_json())

    def update_node(self, path, node):
        return self.run_command("update_node", path, node.to_json())


def main():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description="""\
DESCRIPTION
    Run takler client.""")
    parser.add_argument("-i", "--host", help="server ip address")
    parser.add_argument("-p", "--port", type=int, help="server port number")
    parser.add_argument("--run", nargs=1, metavar='task_path',
                        help="run some task.")
    parser.add_argument("--init", nargs=2, metavar=('task_path', 'task_id'),
                        help="tell the server some task is init with a task id.")
    parser.add_argument("--complete", nargs=1, metavar='task_path',
                        help="complete some task.")
    parser.add_argument("--abort", nargs=1, metavar='task_path',
                        help="abort some task.")
    args = parser.parse_args()

    host = DEFAULT_HOST
    port = DEFAULT_PORT
    if args.host:
        host = args.host
    else:
        print "Using default host: {default_host}".format(default_host=host)
    if args.port:
        port = int(args.port)
    else:
        print "Using default port: {default_port}".format(default_port=port)

    client = Client()
    client.host = host
    client.port = port

    if args.run:
        task_path = args.run[0]
        client.run(task_path)
        pass
    elif args.init:
        task_path = args.init[0]
        task_id = args.init[1]
        client.init(task_path, task_id)
    elif args.complete:
        task_path = args.complete[0]
        client.complete(task_path)
    elif args.abort:
        task_path = args.abort[0]
        client.abort(task_path)


if __name__ == "__main__":
    main()