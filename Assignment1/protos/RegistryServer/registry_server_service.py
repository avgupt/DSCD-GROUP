from concurrent import futures
import logging
import string

import grpc
import RegistryServer_pb2
import RegistryServer_pb2_grpc


class RegisterService(RegistryServer_pb2_grpc.RegistryServerService):

    def RegisterServer(self, request, context):
        server_name = request.server_name
        return RegistryServer_pb2.RegisterServerResponse(status=RegistryServer_pb2.Status.SUCCESS)


def serve():
    port = '50051'
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    RegistryServer_pb2_grpc.add_RegistryServerServiceServicer_to_server(RegisterService(), server)
    server.add_insecure_port('[::]:' + port)
    server.start()
    print("Server started, listening on " + port)
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    serve()