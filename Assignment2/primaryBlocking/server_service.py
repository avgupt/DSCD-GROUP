from concurrent import futures

import grpc
import  server_service_pb2 as server_pb2
import server_service_pb2_grpc as server_pb2_grpc
import registry_server_service_pb2 as registry_server_service_pb2
import registry_server_service_pb2_grpc as registry_server_service_pb2_grpc
from status_pb2 import Status
from time_stamp_pb2 import Date, Time, TimeStamp

class ServerServicer(server_pb2_grpc.ServerServiceServicer):
    def __init__(self, is_primary_replica, primary_replica_ip, primary_replica_port):
        self.is_primary_replica = is_primary_replica
        self.primary_replica_ip = primary_replica_ip
        self.primary_replica_port = primary_replica_port
        self.replicas = [] # primary replica not added
        self.key_value_pairs = {}
        self.path = "/home/dscd-a2/"


    def SendReplicaInfoToPrimary(self, request, context):
        # TODO(shelly): add case for failure
        ip = request.ip
        port = request.port
        address = ip + ':'+ str(port)
        print("SEND REPLICA INFO TO PRIMARY REPLICA REQUEST:",address)
        self.replicas.append(address)
        return server_pb2.SendReplicaInfoToPrimaryResponse(status=server_pb2.SendReplicaInfoToPrimaryResponse.Status.SUCCESS)

    def WriteFromPrimary(self, request, context):
        self.key_value_pairs[request.uuid] = (request.file_name, request.file_content)
        # TODO(manvi): Make the file in the address and write the content and make file_version
        file_version = ""
        return server_pb2.WriteResponse(uuid = request.uuid, version = file_version, status = Status.SUCCESS)

    
    def WriteFromClient(self, request, context):
        if self.is_primary_replica:

            # Case 1: uuid does not exist
            self.key_value_pairs[request.uuid] = (request.file_name, request.file_content)
            # TODO(manvi): Make the file in the address and write the content and make file_version
            file_version = ""
            for i in self.replicas:
                with grpc.insecure_channel(i, options=(('grpc.enable_http_proxy', 0),)) as channel:
                    stub = server_pb2_grpc.ServerServiceStub(channel)       
                    response = stub.WriteFromPrimary(server_pb2.WriteRequest(file_name=request.file_name, file_content=request.file_content, uuid=request.uuid))
                    if response.status != registry_server_service_pb2.Status.SUCCESS:
                        return server_pb2.WriteResponse(uuid = request.uuid, version = file_version, status = Status.FAILURE)
            
            return server_pb2.WriteResponse(uuid = request.uuid, version = file_version, status = Status.SUCCESS)
        
        else:
            with grpc.insecure_channel(self.primary_replica_ip+ ":" +self.primary_replica_port, options=(('grpc.enable_http_proxy', 0),)) as channel:
                stub = server_pb2_grpc.ServerServiceStub(channel)       
                response = stub.WriteFromClient(server_pb2.WriteRequest(file_name=request.file_name, file_content=request.file_content, uuid=request.uuid))

                if response.Status != Status.SUCCESS:
                    return server_pb2.WriteResponse(uuid = request.uuid, version = file_version, status = Status.FAILURE)
                else:
                    return server_pb2.WriteResponse(uuid = request.uuid, version = file_version, status = Status.SUCCESS)


class Server:

    def __init__(self, port):
        self.address = "localhost"
        self.port = port                        # str

    def start(self):
        response = self.__register()
        self.__serve(response.is_replica_primary, response.primary_replica_ip, response.primary_replica_port)

    def __register(self)->bool:
        print("Will try to register to registry server ...")
        with grpc.insecure_channel('localhost:50051') as channel:
            stub = registry_server_service_pb2_grpc.RegistryServerServiceStub(channel)
            
            response = stub.RegisterReplica(registry_server_service_pb2.RegisterReplicaRequest(ip=self.address,port=int(self.port))) 
            print("Is primary",response.is_replica_primary)
            return response
    
    def __serve(self, is_replica_primary, primary_replica_ip, primary_replica_port):

        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        server_pb2_grpc.add_ServerServiceServicer_to_server(
            ServerServicer(is_replica_primary, primary_replica_ip=primary_replica_ip,primary_replica_port=primary_replica_port), server
        )
        server.add_insecure_port("[::]:" + self.port)
        server.start()
        server.wait_for_termination()

if __name__ == "__main__":
    port = input("Enter port for server: ")

    myServer = Server(port)
    myServer.start()
