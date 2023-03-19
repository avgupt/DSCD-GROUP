# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import registry_server_service_pb2 as registry__server__service__pb2
import server_pb2 as server__pb2
import status_pb2 as status__pb2


class RegistryServerServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.getServers = channel.unary_unary(
                '/RegistryServerService/getServers',
                request_serializer=registry__server__service__pb2.Request.SerializeToString,
                response_deserializer=registry__server__service__pb2.Response.FromString,
                )
        self.connect = channel.unary_unary(
                '/RegistryServerService/connect',
                request_serializer=server__pb2.Server.SerializeToString,
                response_deserializer=status__pb2.Status.FromString,
                )


class RegistryServerServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def getServers(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def connect(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_RegistryServerServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'getServers': grpc.unary_unary_rpc_method_handler(
                    servicer.getServers,
                    request_deserializer=registry__server__service__pb2.Request.FromString,
                    response_serializer=registry__server__service__pb2.Response.SerializeToString,
            ),
            'connect': grpc.unary_unary_rpc_method_handler(
                    servicer.connect,
                    request_deserializer=server__pb2.Server.FromString,
                    response_serializer=status__pb2.Status.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'RegistryServerService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class RegistryServerService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def getServers(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/RegistryServerService/getServers',
            registry__server__service__pb2.Request.SerializeToString,
            registry__server__service__pb2.Response.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def connect(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/RegistryServerService/connect',
            server__pb2.Server.SerializeToString,
            status__pb2.Status.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
