# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from takler.server.protocol import takler_pb2 as takler_dot_server_dot_protocol_dot_takler__pb2


class TaklerServerStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.RunInitCommand = channel.unary_unary(
                '/takler_protocol.TaklerServer/RunInitCommand',
                request_serializer=takler_dot_server_dot_protocol_dot_takler__pb2.InitCommand.SerializeToString,
                response_deserializer=takler_dot_server_dot_protocol_dot_takler__pb2.ServiceResponse.FromString,
                )
        self.RunCompleteCommand = channel.unary_unary(
                '/takler_protocol.TaklerServer/RunCompleteCommand',
                request_serializer=takler_dot_server_dot_protocol_dot_takler__pb2.CompleteCommand.SerializeToString,
                response_deserializer=takler_dot_server_dot_protocol_dot_takler__pb2.ServiceResponse.FromString,
                )
        self.RunAbortCommand = channel.unary_unary(
                '/takler_protocol.TaklerServer/RunAbortCommand',
                request_serializer=takler_dot_server_dot_protocol_dot_takler__pb2.AbortCommand.SerializeToString,
                response_deserializer=takler_dot_server_dot_protocol_dot_takler__pb2.ServiceResponse.FromString,
                )
        self.RunEventCommand = channel.unary_unary(
                '/takler_protocol.TaklerServer/RunEventCommand',
                request_serializer=takler_dot_server_dot_protocol_dot_takler__pb2.EventCommand.SerializeToString,
                response_deserializer=takler_dot_server_dot_protocol_dot_takler__pb2.ServiceResponse.FromString,
                )
        self.RunMeterCommand = channel.unary_unary(
                '/takler_protocol.TaklerServer/RunMeterCommand',
                request_serializer=takler_dot_server_dot_protocol_dot_takler__pb2.MeterCommand.SerializeToString,
                response_deserializer=takler_dot_server_dot_protocol_dot_takler__pb2.ServiceResponse.FromString,
                )
        self.RunRequeueCommand = channel.unary_unary(
                '/takler_protocol.TaklerServer/RunRequeueCommand',
                request_serializer=takler_dot_server_dot_protocol_dot_takler__pb2.RequeueCommand.SerializeToString,
                response_deserializer=takler_dot_server_dot_protocol_dot_takler__pb2.ServiceResponse.FromString,
                )
        self.RunShowRequest = channel.unary_unary(
                '/takler_protocol.TaklerServer/RunShowRequest',
                request_serializer=takler_dot_server_dot_protocol_dot_takler__pb2.ShowRequest.SerializeToString,
                response_deserializer=takler_dot_server_dot_protocol_dot_takler__pb2.ShowResponse.FromString,
                )


class TaklerServerServicer(object):
    """Missing associated documentation comment in .proto file."""

    def RunInitCommand(self, request, context):
        """child command
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def RunCompleteCommand(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def RunAbortCommand(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def RunEventCommand(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def RunMeterCommand(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def RunRequeueCommand(self, request, context):
        """control command

        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def RunShowRequest(self, request, context):
        """query command

        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_TaklerServerServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'RunInitCommand': grpc.unary_unary_rpc_method_handler(
                    servicer.RunInitCommand,
                    request_deserializer=takler_dot_server_dot_protocol_dot_takler__pb2.InitCommand.FromString,
                    response_serializer=takler_dot_server_dot_protocol_dot_takler__pb2.ServiceResponse.SerializeToString,
            ),
            'RunCompleteCommand': grpc.unary_unary_rpc_method_handler(
                    servicer.RunCompleteCommand,
                    request_deserializer=takler_dot_server_dot_protocol_dot_takler__pb2.CompleteCommand.FromString,
                    response_serializer=takler_dot_server_dot_protocol_dot_takler__pb2.ServiceResponse.SerializeToString,
            ),
            'RunAbortCommand': grpc.unary_unary_rpc_method_handler(
                    servicer.RunAbortCommand,
                    request_deserializer=takler_dot_server_dot_protocol_dot_takler__pb2.AbortCommand.FromString,
                    response_serializer=takler_dot_server_dot_protocol_dot_takler__pb2.ServiceResponse.SerializeToString,
            ),
            'RunEventCommand': grpc.unary_unary_rpc_method_handler(
                    servicer.RunEventCommand,
                    request_deserializer=takler_dot_server_dot_protocol_dot_takler__pb2.EventCommand.FromString,
                    response_serializer=takler_dot_server_dot_protocol_dot_takler__pb2.ServiceResponse.SerializeToString,
            ),
            'RunMeterCommand': grpc.unary_unary_rpc_method_handler(
                    servicer.RunMeterCommand,
                    request_deserializer=takler_dot_server_dot_protocol_dot_takler__pb2.MeterCommand.FromString,
                    response_serializer=takler_dot_server_dot_protocol_dot_takler__pb2.ServiceResponse.SerializeToString,
            ),
            'RunRequeueCommand': grpc.unary_unary_rpc_method_handler(
                    servicer.RunRequeueCommand,
                    request_deserializer=takler_dot_server_dot_protocol_dot_takler__pb2.RequeueCommand.FromString,
                    response_serializer=takler_dot_server_dot_protocol_dot_takler__pb2.ServiceResponse.SerializeToString,
            ),
            'RunShowRequest': grpc.unary_unary_rpc_method_handler(
                    servicer.RunShowRequest,
                    request_deserializer=takler_dot_server_dot_protocol_dot_takler__pb2.ShowRequest.FromString,
                    response_serializer=takler_dot_server_dot_protocol_dot_takler__pb2.ShowResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'takler_protocol.TaklerServer', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class TaklerServer(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def RunInitCommand(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/takler_protocol.TaklerServer/RunInitCommand',
            takler_dot_server_dot_protocol_dot_takler__pb2.InitCommand.SerializeToString,
            takler_dot_server_dot_protocol_dot_takler__pb2.ServiceResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def RunCompleteCommand(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/takler_protocol.TaklerServer/RunCompleteCommand',
            takler_dot_server_dot_protocol_dot_takler__pb2.CompleteCommand.SerializeToString,
            takler_dot_server_dot_protocol_dot_takler__pb2.ServiceResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def RunAbortCommand(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/takler_protocol.TaklerServer/RunAbortCommand',
            takler_dot_server_dot_protocol_dot_takler__pb2.AbortCommand.SerializeToString,
            takler_dot_server_dot_protocol_dot_takler__pb2.ServiceResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def RunEventCommand(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/takler_protocol.TaklerServer/RunEventCommand',
            takler_dot_server_dot_protocol_dot_takler__pb2.EventCommand.SerializeToString,
            takler_dot_server_dot_protocol_dot_takler__pb2.ServiceResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def RunMeterCommand(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/takler_protocol.TaklerServer/RunMeterCommand',
            takler_dot_server_dot_protocol_dot_takler__pb2.MeterCommand.SerializeToString,
            takler_dot_server_dot_protocol_dot_takler__pb2.ServiceResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def RunRequeueCommand(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/takler_protocol.TaklerServer/RunRequeueCommand',
            takler_dot_server_dot_protocol_dot_takler__pb2.RequeueCommand.SerializeToString,
            takler_dot_server_dot_protocol_dot_takler__pb2.ServiceResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def RunShowRequest(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/takler_protocol.TaklerServer/RunShowRequest',
            takler_dot_server_dot_protocol_dot_takler__pb2.ShowRequest.SerializeToString,
            takler_dot_server_dot_protocol_dot_takler__pb2.ShowResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
