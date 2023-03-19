from __future__ import print_function

import grpc
import uuid

import server_service_pb2 as server_pb2
import server_service_pb2_grpc as server_pb2_grpc


import registry_server_service_pb2 as registry_server_service_pb2
import registry_server_service_pb2_grpc as registry_server_service_pb2_grpc


class Client:

    # RPC from client to Registry server
    def getReplicaListFromRegistryServer(self):
        with grpc.insecure_channel('localhost:50051') as channel:
            stub = registry_server_service_pb2_grpc.RegistryServerServiceStub(channel)
            response = stub.GetReplicaList(registry_server_service_pb2.GetReplicaListRequest())
            print(response.servers)
            channel.close()
            return response

if __name__== "__main__":
    myClient = Client()
    myClient.getReplicaListFromRegistryServer()
