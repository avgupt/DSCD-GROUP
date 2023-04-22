from concurrent import futures

import grpc
import  mapper_service_pb2 as mapper_pb2
import mapper_service_pb2_grpc as mapper_pb2_grpc

from pathlib import Path
import datetime
import os
import sys

class MapperServiceServicer(mapper_pb2_grpc.MapperServiceServicer):
    def __init__(self, mapper_name):
        self.mapper_name = mapper_name
        self.path = "folders\\" + "ID_" + mapper_name
        self.intermediate_data = {}
        Path(self.path).mkdir(parents=True, exist_ok=True)
    
    def file_read(self, path):
        with open(path, "r") as file:
            file_content = file.read()
        return file_content
    
    def file_write(self, path, content):
        with open(path, "a+") as file:
            file.write(content + "\n")

    def partition(self, query, key, r):
        if (query == 1):
            partition_number = len(key)%r

        # TODO(Avishi): Partition functions for others
        return str(partition_number)
    
    def _wordCount(self, request):
        #TODO(Manvi): Implement line wise processing if needed
        for file_name in request.input_split_files:
            file_content = self.file_read(request.input_location + "\\" + file_name).split()

            for key in file_content:
                value = 1
                partion_name = self.partition(request.query, key, request.n_reducers)
                self.file_write(self.path + "\\P" + partion_name, key + " " + str(value))
                
        return mapper_pb2.MapResponse(intermediate_file_location = self.path, status = mapper_pb2.MapResponse.Status.SUCCESS)

    def map(self, request, context):
        
        if request.query == 1:
            return self._wordCount(request)
        
        # TODO(Avishi): Other Function
        elif request.query == 2:
            return self._invertedIndex(request)
        

        return self._naturalJoin(request)


class Mapper:

    def __init__(self, port, mapper_name):
        self.address = "localhost"
        self.port = port                        # str
        self.mapper_name = mapper_name
    
    def serve(self, mapper_name):

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
    mapper_name = sys.argv[2]
    myServer = Mapper(port, mapper_name)
    myServer.serve(mapper_name)