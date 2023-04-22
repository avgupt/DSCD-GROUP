from concurrent import futures

import grpc
import  mapper_service_pb2 as mapper_pb2
import mapper_service_pb2_grpc as mapper_pb2_grpc
import master_service_pb2 as master_service_pb2 
import master_service_pb2_grpc as master_service_pb2_grpc

from pathlib import Path
import datetime
import os
import sys

class MapperServiceServicer(mapper_pb2_grpc.MapperServiceServicer):
    def __init__(self, mapper_name):
        self.mapper_name = mapper_name
        self.query = 1
    
    def _wordCount():
        return  

    def _map(self):
        # Word Count
        if (self.query == 1):
            return self._wordCount()
        elif (self.query == 2):
            return self._invertedIndex()
        elif (self.query == 3):
            return self._naturalJoin()
        elif (self.query == 4):
            return self._customFunction()
        return 


class Mapper:

    def __init__(self, port):
        self.address = "localhost"
        self.port = port                        # str

    def start(self):
        response = self.__register()
        self.__serve(response.mapper_name)

    def __register(self)->bool:
        print("Will try to register to master ...")
        with grpc.insecure_channel('localhost:50051') as channel:
            stub = master_service_pb2_grpc.MasterServiceStub(channel)
            response = stub.RegisterMapper(master_service_pb2.RegisterMapperRequest(ip=self.address,port=int(self.port))) 
            print(response.mapper_name)
            return response

    
    def __serve(self, mapper_name):

        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        mapper_pb2_grpc.add_MapperServiceServicer_to_server(
            MapperServiceServicer(mapper_name), server
        )
        server.add_insecure_port("[::]:" + self.port)
        server.start()
        server.wait_for_termination()

if __name__ == "__main__":
    # port = input("Enter port for server: ")
    port = sys.argv[1]
    myServer = Mapper(port)
    myServer.start()