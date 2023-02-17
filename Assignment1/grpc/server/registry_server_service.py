from concurrent import futures
import logging

import grpc
import registry_server_service_pb2 as registry_server_service_pb2 
import registry_server_service_pb2_grpc as registry_server_service_pb2_grpc


max_servers = 10
servers = {}

class RegisterService(registry_server_service_pb2_grpc.RegistryServerServiceServicer):

    def RegisterServer(self, request, context):
        # Assuming server_name would be unique, otherwise it can override servers map
        server_name = request.server_name
        ip = request.ip
        port = request.port
        address = ip + ':'+ str(port)
        print("JOIN REQUEST FROM", address)
        if len(servers) < max_servers:
            servers[server_name] = address
            print("Server registered to RegistryServer, server name:",server_name)
            return registry_server_service_pb2.RegisterServerResponse(status=registry_server_service_pb2.Status.SUCCESS)
        return registry_server_service_pb2.RegisterServerResponse(status=registry_server_service_pb2.Status.FAILED)

    def GetServerList(self, request, context):
        print("SERVICE LIST REQUEST FROM", request.client_uuid)
        return registry_server_service_pb2.GetServerListResponse(servers=servers)


def serve():
    port = '50051'
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    registry_server_service_pb2_grpc.add_RegistryServerServiceServicer_to_server(RegisterService(), server)
    server.add_insecure_port('[::]:' + port)
    server.start()
    print("Registry Server started, listening on " + port)
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    serve()