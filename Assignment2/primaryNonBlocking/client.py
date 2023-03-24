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
        with grpc.insecure_channel(server_path, options=(('grpc.enable_http_proxy', 0),)) as channel:
            stub = server_pb2_grpc.ServerServiceStub(channel)
            response_stream= stub.writeFromClient(server_pb2.WriteRequest(file_name=file_name, file_content=file_content, uuid=uuid))
            response = next(response_stream)
            if response.status.type == Status.STATUS_TYPE.SUCCESS:
                print("Status : SUCCESS")
                print("UUID :", response.uuid)
                print("Version :", self.printVersion(response.version))
            
            else:
                print("Status : FAILURE")
                print("Reason :", response.status.message)
            response_stream.cancel()

    def delete(self, uuid, server_path):
        with grpc.insecure_channel(server_path, options=(('grpc.enable_http_proxy', 0),)) as channel:
            stub = server_pb2_grpc.ServerServiceStub(channel)
            response_stream = stub.deleteFromClient(server_pb2.DeleteRequest(uuid=uuid))
            response = next(response_stream)
            if response.type == Status.STATUS_TYPE.SUCCESS:
                print("Status : SUCCESS")
            else:
                print("Status : FAILURE")
                print("Reason :", response.message)
            response_stream.cancel()


    def read(self, uuid, server_path):
        with grpc.insecure_channel(server_path, options=(('grpc.enable_http_proxy', 0),)) as channel:
            stub = server_pb2_grpc.ServerServiceStub(channel)
            response = stub.read(server_pb2.ReadRequest(uuid=uuid))
            if response.status.type == Status.STATUS_TYPE.SUCCESS:
                print("Status : SUCCESS")
                print("File name :", response.file_name)
                print("Content :", response.content)
                print("Version :", self.printVersion(response.version))
            else:
                print("Status : FAILURE")
                print("Reason :", response.status.message) #Doubt: Shouldn't this be response.status.message?
        

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
                # file_uuid_no = input("Enter file number: ")
                # file_uuid = file_dict[file_uuid_no]
                file_uuid = input("Enter file uuid: ")
                myClient.read(file_uuid, server_name)

            elif n == 4: 
                file_uuid = input("Enter file uuid: ")
                # file_uuid_no = int(input("Enter file number (in order of file written): "))
                # file_uuid = file_dict[file_uuid_no]
                # file_uuid = str(uuid.uuid1()) #Trial for Case 1: delete
                myClient.delete(file_uuid, server_name)

            else:
                # file_uuid_no = int(input("Enter file number (in order of file written): "))
                # file_uuid = file_dict[file_uuid_no]
                file_uuid = input("Enter file uuid: ")
                file_name = input("Enter the same file name ([name].txt): ")
                file_content = input("Enter file content: ")
                myClient.write(file_name, file_content, file_uuid, server_name)
