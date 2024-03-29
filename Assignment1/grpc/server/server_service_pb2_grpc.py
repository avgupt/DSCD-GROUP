# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import server_service_pb2 as grpc_dot_server_dot_server__service__pb2


class ClientServerStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.GetArticles = channel.unary_unary(
                '/ClientServer/GetArticles',
                request_serializer=grpc_dot_server_dot_server__service__pb2.GetArticlesRequest.SerializeToString,
                response_deserializer=grpc_dot_server_dot_server__service__pb2.GetArticlesResponse.FromString,
                )
        self.PublishArticle = channel.unary_unary(
                '/ClientServer/PublishArticle',
                request_serializer=grpc_dot_server_dot_server__service__pb2.PublishArticleRequest.SerializeToString,
                response_deserializer=grpc_dot_server_dot_server__service__pb2.PublishArticleResponse.FromString,
                )
        self.ClientServerJoinServer = channel.unary_unary(
                '/ClientServer/ClientServerJoinServer',
                request_serializer=grpc_dot_server_dot_server__service__pb2.ClientServerJoinServerRequest.SerializeToString,
                response_deserializer=grpc_dot_server_dot_server__service__pb2.ClientServerJoinServerResponse.FromString,
                )
        self.JoinServer = channel.unary_unary(
                '/ClientServer/JoinServer',
                request_serializer=grpc_dot_server_dot_server__service__pb2.ServerJoinRequest.SerializeToString,
                response_deserializer=grpc_dot_server_dot_server__service__pb2.ServerJoinResponse.FromString,
                )
        self.LeaveServer = channel.unary_unary(
                '/ClientServer/LeaveServer',
                request_serializer=grpc_dot_server_dot_server__service__pb2.ServerLeaveRequest.SerializeToString,
                response_deserializer=grpc_dot_server_dot_server__service__pb2.ServerLeaveResponse.FromString,
                )


class ClientServerServicer(object):
    """Missing associated documentation comment in .proto file."""

    def GetArticles(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def PublishArticle(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ClientServerJoinServer(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def JoinServer(self, request, context):
        """Manvi RPCs
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def LeaveServer(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_ClientServerServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'GetArticles': grpc.unary_unary_rpc_method_handler(
                    servicer.GetArticles,
                    request_deserializer=grpc_dot_server_dot_server__service__pb2.GetArticlesRequest.FromString,
                    response_serializer=grpc_dot_server_dot_server__service__pb2.GetArticlesResponse.SerializeToString,
            ),
            'PublishArticle': grpc.unary_unary_rpc_method_handler(
                    servicer.PublishArticle,
                    request_deserializer=grpc_dot_server_dot_server__service__pb2.PublishArticleRequest.FromString,
                    response_serializer=grpc_dot_server_dot_server__service__pb2.PublishArticleResponse.SerializeToString,
            ),
            'ClientServerJoinServer': grpc.unary_unary_rpc_method_handler(
                    servicer.ClientServerJoinServer,
                    request_deserializer=grpc_dot_server_dot_server__service__pb2.ClientServerJoinServerRequest.FromString,
                    response_serializer=grpc_dot_server_dot_server__service__pb2.ClientServerJoinServerResponse.SerializeToString,
            ),
            'JoinServer': grpc.unary_unary_rpc_method_handler(
                    servicer.JoinServer,
                    request_deserializer=grpc_dot_server_dot_server__service__pb2.ServerJoinRequest.FromString,
                    response_serializer=grpc_dot_server_dot_server__service__pb2.ServerJoinResponse.SerializeToString,
            ),
            'LeaveServer': grpc.unary_unary_rpc_method_handler(
                    servicer.LeaveServer,
                    request_deserializer=grpc_dot_server_dot_server__service__pb2.ServerLeaveRequest.FromString,
                    response_serializer=grpc_dot_server_dot_server__service__pb2.ServerLeaveResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'ClientServer', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class ClientServer(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def GetArticles(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/ClientServer/GetArticles',
            grpc_dot_server_dot_server__service__pb2.GetArticlesRequest.SerializeToString,
            grpc_dot_server_dot_server__service__pb2.GetArticlesResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def PublishArticle(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/ClientServer/PublishArticle',
            grpc_dot_server_dot_server__service__pb2.PublishArticleRequest.SerializeToString,
            grpc_dot_server_dot_server__service__pb2.PublishArticleResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def ClientServerJoinServer(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/ClientServer/ClientServerJoinServer',
            grpc_dot_server_dot_server__service__pb2.ClientServerJoinServerRequest.SerializeToString,
            grpc_dot_server_dot_server__service__pb2.ClientServerJoinServerResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def JoinServer(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/ClientServer/JoinServer',
            grpc_dot_server_dot_server__service__pb2.ServerJoinRequest.SerializeToString,
            grpc_dot_server_dot_server__service__pb2.ServerJoinResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def LeaveServer(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/ClientServer/LeaveServer',
            grpc_dot_server_dot_server__service__pb2.ServerLeaveRequest.SerializeToString,
            grpc_dot_server_dot_server__service__pb2.ServerLeaveResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
