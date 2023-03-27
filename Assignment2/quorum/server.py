from concurrent import futures
import logging, os, random, shutil

import grpc
import protos.registry_server_service_pb2 as registry_server_service_pb2 
import protos.registry_server_service_pb2_grpc as registry_server_service_pb2_grpc
import protos.server_service_pb2 as server_service_pb2
import protos.server_service_pb2_grpc as server_service_pb2_grpc

from protos.server_pb2 import Server as Server_proto
from protos.status_pb2 import Status

class ServerService(server_service_pb2_grpc.ServerServiceServicer):

    def write(self, request, context):
        return super().write(request, context)
    
    def read(self, request, context):
        return super().read(request, context)
    
    def delete(self, request, context):
        return super().delete(request, context)

class Server:

    def __init__(self, port) -> None:
        self.ip = "localhost"
        self.port = port
        self.memory_map = {}
        self.connection_status = self.__register_server()
    
    def __create_folder(self, port):
        data_path = "datastore/" + port + "/"

        if os.path.exists(data_path):
            # Delete entire datastore if exists already.
            # Assumptions:
            #   Two servers cannot run on the same port.
            #   Entire system shuts down if there is a failure.  
            shutil.rmtree(data_path)
        
        os.makedirs(data_path)
        print("Files for localhost:" + self.port + " are being stored in the folder " + data_path)
        return data_path
    
    def __register_server(self):
        print("Connecting to Registry Server...")
        with grpc.insecure_channel('localhost:8888') as channel:
            stub = registry_server_service_pb2_grpc.RegistryServerServiceStub(channel)
            
            response = stub.connect(Server_proto(ip=self.ip, port=self.port))
            if response.type == Status.STATUS_TYPE.SUCCESS:
                print("SUCCESS")
                return True

        print("FAILURE")
        return False
    
    def __serve(self):
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        server_service_pb2_grpc.add_ServerServiceServicer_to_server(ServerService(), server)
        server.add_insecure_port('[::]:' + self.port)
        server.start()
        print("Server started, listening on " + self.port)
        server.wait_for_termination()
    
    def start(self):
        if self.connection_status:
            self.datastore_path = self.__create_folder(self.port)
            return self.__serve()
        
if __name__ == "__main__":
    port = input("Enter port for server: ")
    
    myServer = Server(port)
    myServer.start()
