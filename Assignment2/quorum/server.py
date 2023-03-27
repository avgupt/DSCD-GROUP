from concurrent import futures
import logging, os, random, shutil
from datetime import datetime

import grpc
import protos.registry_server_service_pb2 as registry_server_service_pb2 
import protos.registry_server_service_pb2_grpc as registry_server_service_pb2_grpc
import protos.server_service_pb2 as server_service_pb2
import protos.server_service_pb2_grpc as server_service_pb2_grpc

from protos.server_pb2 import Server as Server_proto
from protos.status_pb2 import Status
from protos.server_service_pb2 import WriteResponse, ReadResponse
from protos.time_stamp_pb2 import TimeStamp, Date, Time

memory_map = {}

class ServerService(server_service_pb2_grpc.ServerServiceServicer):

    def __get_timestamp(self):
        datetime_ = datetime.now()
        date_ = Date(
            day=datetime_.day,
            month=datetime_.month,
            year=datetime_.year
        )
        time_ = Time(
            hour=datetime_.hour,
            minute=datetime_.minute,
            second=datetime_.second
        )
        return TimeStamp(date=date_, time=time_)
    
    def __write_file(self, file_path, content):
        f = open(file_path, "w")
        f.write(content)
        f.close()
    
    def __send_write_failure(self, message):
        return WriteResponse(
            status=Status(
                type=Status.STATUS_TYPE.FAILURE,
                message=message
            )
        )

    def write(self, request, context):
        file_path = data_path + request.file_name + ".txt"
        is_in_map = request.uuid in memory_map.keys()
        is_in_system = os.path.exists(file_path)

        if is_in_map:
            if not is_in_system or memory_map[request.uuid][0] == "":
                return self.__send_write_failure("DELETED FILE CANNOT BE UPDATED")
            elif request.file_name != memory_map[request.uuid][0]:
                return self.__send_write_failure("FILE NAME MISMATCH")
        elif is_in_system:
            return self.__send_write_failure("FILE WITH THE SAME NAME ALREADY EXISTS")
            
        version_ = self.__get_timestamp()
        memory_map[request.uuid] = [request.file_name, version_]
        self.__write_file(file_path, request.file_content)
        return WriteResponse(
            uuid=request.uuid,
            version=version_,
            status=Status(type=Status.STATUS_TYPE.SUCCESS)
        )
    
    def __send_read_failure(self, message):
        return ReadResponse(
            status=Status(
            type=Status.STATUS_TYPE.FAILURE,
            message=message                    
            )
        )
    
    def read(self, request, context):
        is_in_map = request.uuid in memory_map.keys()

        if not is_in_map:
            return self.__send_read_failure("FILE DOES NOT EXIST")

        file_path = data_path + memory_map[request.uuid][0] + ".txt"
        if memory_map[request.uuid][0] == "" or not os.path.exists(file_path):
            return self.__send_read_failure("FILE ALREADY DELETED")

        f = open(file_path, "r")
        file_content= f.read()
        f.close()      
        return ReadResponse(
            file_name=memory_map[request.uuid][0],
            content=file_content,
            version=memory_map[request.uuid][1],
            status=Status(type=Status.STATUS_TYPE.SUCCESS)
        )
    
    def delete(self, request, context):
        is_in_map = request.uuid in memory_map.keys()
        version_ = self.__get_timestamp()

        if not is_in_map:
            memory_map[request.uuid] = ["", version_]
            return Status(
                type=Status.STATUS_TYPE.FAILURE,
                message="FILE DOES NOT EXIST"
            )
        
        file_path = data_path + memory_map[request.uuid][0] + ".txt"
        if not os.path.exists(file_path):
            return Status(
                type=Status.STATUS_TYPE.FAILURE,
                message="FILE ALREADY DELETED"
            )
        
        os.remove(file_path)
        memory_map[request.uuid] = ["", version_]
        return Status(type=Status.STATUS_TYPE.SUCCESS)

class Server:

    def __init__(self, port) -> None:
        self.ip = "localhost"
        self.port = port
        self.connection_status = self.__register_server()
        self.datastore_path = self.__create_folder(self.port)
    
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
            return self.__serve()


if __name__ == "__main__":
    port = input("Enter port for server: ")

    myServer = Server(port)
    data_path = myServer.datastore_path
    myServer.start()
