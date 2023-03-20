from concurrent import futures

import grpc
import  server_service_pb2 as server_pb2
import server_service_pb2_grpc as server_pb2_grpc
import registry_server_service_pb2 as registry_server_service_pb2
import registry_server_service_pb2_grpc as registry_server_service_pb2_grpc
from status_pb2 import Status
from time_stamp_pb2 import Date, Time, TimeStamp
from pathlib import Path
import datetime


class ServerServicer(server_pb2_grpc.ServerServiceServicer):
    def __init__(self, is_primary_replica, primary_replica_ip, primary_replica_port,replica_name):
        self.is_primary_replica = is_primary_replica
        self.primary_replica_ip = primary_replica_ip
        self.primary_replica_port = primary_replica_port
        self.replicas = [] # primary replica not added
        self.key_value_pairs = {}
        self.path = "folders\\" + replica_name
        Path(self.path).mkdir(parents=True, exist_ok=True)
        

    def SendReplicaInfoToPrimary(self, request, context):
        # TODO(shelly): add case for failure
        ip = request.ip
        port = request.port
        address = ip + ':'+ str(port)
        print("SEND REPLICA INFO TO PRIMARY REPLICA REQUEST:",address)
        self.replicas.append(address)
        return server_pb2.SendReplicaInfoToPrimaryResponse(status=server_pb2.SendReplicaInfoToPrimaryResponse.Status.SUCCESS)

    def writeInFile(self, file_name, file_content):
        with open(self.path + "\\" + file_name, "w") as file:
            file.write(file_content)
        
        x = datetime.datetime.now()
        d = Date(day=11, month=12, year=2023)
        t = Time(hour=11, minute=51, second=11)
        file_version = TimeStamp(date=d, time=t)
        return file_version
    
    def write(self, request, context):
        # TODO(manvi): Add other write cases
        if request.is_write_from_client == 1:
            if self.is_primary_replica:

                # Case 1: uuid does not exist
                self.key_value_pairs[request.uuid] = (request.file_name, request.file_content)
                file_version = self.writeInFile(request.file_name, request.file_content)

                for i in self.replicas:
                    with grpc.insecure_channel(i, options=(('grpc.enable_http_proxy', 0),)) as channel:
                        stub = server_pb2_grpc.ServerServiceStub(channel)       
                        response = stub.write(server_pb2.WriteRequest(file_name=request.file_name, file_content=request.file_content, uuid=request.uuid, is_write_from_client=0))

                        if response.status.type != Status.STATUS_TYPE.SUCCESS:
                            return server_pb2.WriteResponse(uuid=request.uuid, version=file_version, status=Status(type=Status.STATUS_TYPE.FAILURE))
                
                return server_pb2.WriteResponse(uuid=request.uuid, version=file_version, status=Status(type=Status.STATUS_TYPE.SUCCESS))
            
            else:
                with grpc.insecure_channel(str(self.primary_replica_ip)+ ":" +str(self.primary_replica_port), options=(('grpc.enable_http_proxy', 0),)) as channel:
                    stub = server_pb2_grpc.ServerServiceStub(channel)       
                    response = stub.write(server_pb2.WriteRequest(file_name=request.file_name, file_content=request.file_content, uuid=request.uuid, is_write_from_client=1))

                    if response.status.type != Status.STATUS_TYPE.SUCCESS:
                        return server_pb2.WriteResponse(uuid=request.uuid, version=response.version, status=Status(type=Status.STATUS_TYPE.FAILURE))
                    else:
                        return server_pb2.WriteResponse(uuid=request.uuid, version=response.version, status=Status(type=Status.STATUS_TYPE.SUCCESS))

        else:
            self.key_value_pairs[request.uuid] = (request.file_name, request.file_content)
            file_version = self.writeInFile(request.file_name, request.file_content)
            return server_pb2.WriteResponse(uuid=request.uuid, version=file_version, status=Status(type=Status.STATUS_TYPE.SUCCESS))

class Server:

    def __init__(self, port):
        self.address = "localhost"
        self.port = port                        # str

    def start(self):
        response = self.__register()
        self.__serve(response.is_replica_primary, response.primary_replica_ip, response.primary_replica_port, response.replica_name)

    def __register(self)->bool:
        print("Will try to register to registry server ...")
        with grpc.insecure_channel('localhost:50051') as channel:
            stub = registry_server_service_pb2_grpc.RegistryServerServiceStub(channel)
            
            response = stub.RegisterReplica(registry_server_service_pb2.RegisterReplicaRequest(ip=self.address,port=int(self.port))) 
            print(response.replica_name)
            print("Is primary",response.is_replica_primary)
            return response
    
    def __serve(self, is_replica_primary, primary_replica_ip, primary_replica_port,replica_name):

        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        server_pb2_grpc.add_ServerServiceServicer_to_server(
            ServerServicer(is_replica_primary, primary_replica_ip=primary_replica_ip,primary_replica_port=primary_replica_port,replica_name=replica_name), server
        )
        server.add_insecure_port("[::]:" + self.port)
        server.start()
        server.wait_for_termination()

if __name__ == "__main__":
    port = input("Enter port for server: ")

    myServer = Server(port)
    myServer.start()
