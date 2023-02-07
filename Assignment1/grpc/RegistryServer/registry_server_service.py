from concurrent import futures
import logging

import grpc
import registry_server_service_pb2 
import registry_server_service_pb2_grpc


class RegisterService(registry_server_service_pb2_grpc.RegistryServerService):

    def RegisterServer(self, request, context):
        # TODO: Update the actual implementation of RegisterServer here
        server_name = request.server_name
        return registry_server_service_pb2.RegisterServerResponse(status=registry_server_service_pb2.Status.SUCCESS)


def serve():
    port = '50051'
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    registry_server_service_pb2_grpc.add_RegistryServerServiceServicer_to_server(RegisterService(), server)
    server.add_insecure_port('[::]:' + port)
    server.start()
    print("Server started, listening on " + port)
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    serve()