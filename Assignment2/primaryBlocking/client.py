from __future__ import print_function

import grpc
import uuid

import server_service_pb2 as server_pb2
import server_service_pb2_grpc as server_pb2_grpc


import registry_server_service_pb2 as registry_server_service_pb2
import registry_server_service_pb2_grpc as registry_server_service_pb2_grpc

from status_pb2 import Status


class Client:

    # RPC from client to Registry server
    def getReplicaListFromRegistryServer(self):
        with grpc.insecure_channel('localhost:50051') as channel:
            stub = registry_server_service_pb2_grpc.RegistryServerServiceStub(channel)
            response = stub.GetReplicaList(registry_server_service_pb2.GetReplicaListRequest())
            print(response.servers)
            channel.close()
            return response

    def printVersion(self, version):
        version_in_str = str(version.date.day)+"/"+str(version.date.month)+"/"+str(version.date.year)+" "+str(version.time.hour)+":"+str(version.time.minute)+":"+str(version.time.second)
        return version_in_str

    def write(self, file_name, file_content, uuid, server_path):
        with grpc.insecure_channel('localhost:8081', options=(('grpc.enable_http_proxy', 0),)) as channel:
            stub = server_pb2_grpc.ServerServiceStub(channel)
            response = stub.write(server_pb2.WriteRequest(file_name=file_name, file_content=file_content, uuid=uuid, is_write_from_client=1))
            if response.status.type == Status.STATUS_TYPE.SUCCESS:
                print("Status : SUCCESS")
                print("UUID :", response.uuid)
                print("Version :", self.printVersion(response.version))
            
            else:
                print("Status : FAILURE")
                print("Reason :", response.status.message)
        

if __name__== "__main__":
    myClient = Client()
    file_dict = {}
    count = 0
    
    while(True):
        print()
        print("GetReplicaList[1], Write[2], Read[3], Delete[4], Update[5]:")
        n = int(input())

        if n == 1:
            myClient.getReplicaListFromRegistryServer()
        
        elif n > 5:
            print("INVALID REQUEST")
        else:
            server_name = input("Enter server port: ")
            server_name = "localhost:"+server_name

            if n == 2:
                count+=1
                file_name = input("Enter file name ([name].txt): ")
                file_content = input("Enter file content: ")
                file_uuid = str(uuid.uuid1())
                file_dict[count] = file_uuid
                myClient.write(file_name, file_content, file_uuid, server_name)

            elif n == 3:
                file_uuid_no = input("Enter file number: ")
                file_uuid = file_dict[file_uuid_no]
                # myClient.read(file_uuid, server_name)

            elif n == 4: 
                file_uuid_no = input("Enter file number: ")
                file_uuid = file_dict[file_uuid_no]
                # myClient.delete(file_uuid, server_name)

    