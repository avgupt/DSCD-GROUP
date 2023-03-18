from concurrent import futures
from datetime import date
import logging
import datetime

import grpc
import  server_service_pb2 as server_pb2
import server_service_pb2_grpc as server_pb2_grpc
import registry_server_service_pb2 as registry_server_service_pb2
import registry_server_service_pb2_grpc as registry_server_service_pb2_grpc

class ClientServerServicer(server_pb2_grpc.ClientServerServicer):
    def __init__(self, server_name, is_primary_replica, primary_replica_ip, primary_replica_port):
        self.name = server_name
        self.is_primary_replica = is_primary_replica
        self.primary_replica_ip = primary_replica_ip
        self.primary_replica_port = primary_replica_port

class Server:

    def __init__(self, port,server_name):
        self.address = "localhost"
        self.port = port                        # str
        self.name = server_name

    def start(self):
        response = self.__register()
        self.__serve(response.is_replica_primary, response.primary_replica_ip, response.primary_replica_port)

    def __register(self)->bool:
        print("Will try to register to registry server ...")
        with grpc.insecure_channel('localhost:50051') as channel:
            stub = registry_server_service_pb2_grpc.RegistryServerServiceStub(channel)
            
            response = stub.RegisterReplica(registry_server_service_pb2.RegisterReplicaRequest(replica_name=self.name,ip=self.address,port=int(self.port))) 
            print("Is primary",response.is_replica_primary)
            return response
    
    def __serve(self,is_replica_primary,primary_replica_ip,primary_replica_port):

        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        server_pb2_grpc.add_ClientServerServicer_to_server(
            ClientServerServicer(self.name, is_replica_primary, primary_replica_ip=primary_replica_ip,primary_replica_port=primary_replica_port), server
        )
        server.add_insecure_port("[::]:" + self.port)
        server.start()
        server.wait_for_termination()

if __name__ == "__main__":
    port = input("Enter port for server: ")
    server_name = input("Enter server name: ")

    myServer = Server(port,server_name)
    myServer.start()
