# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import reducer_service_pb2 as reducer__service__pb2


class ReducerServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.reduce = channel.unary_unary(
                '/ReducerService/reduce',
                request_serializer=reducer__service__pb2.ReduceRequest.SerializeToString,
                response_deserializer=reducer__service__pb2.ReduceResponse.FromString,
                )


class ReducerServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def reduce(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_ReducerServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'reduce': grpc.unary_unary_rpc_method_handler(
                    servicer.reduce,
                    request_deserializer=reducer__service__pb2.ReduceRequest.FromString,
                    response_serializer=reducer__service__pb2.ReduceResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'ReducerService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class ReducerService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def reduce(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/ReducerService/reduce',
            reducer__service__pb2.ReduceRequest.SerializeToString,
            reducer__service__pb2.ReduceResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
