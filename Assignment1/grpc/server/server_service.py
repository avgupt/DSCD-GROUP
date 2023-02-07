import ServerService_pb2, ServerService_pb2_grpc

class ServerService(ServerService_pb2.ServerService):

    def GetArticles(self, request, context):
        pass
