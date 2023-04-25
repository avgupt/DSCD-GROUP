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
        self.n_reducers = 0
        self.query = 0
        Path(self.path).mkdir(parents=True, exist_ok=True)
    
    def file_read(self, path):
        with open(path, "r") as file:
            file_content = file.read().splitlines()
        return file_content
    
    def file_write(self, path, content):
        with open(path, "a+") as file:
            file.write(content + "\n")

    def partition(self, key):
        if (self.query < 3):
            partition_number = len(key)%(self.n_reducers)

        # TODO(Avishi): Partition functions for others
        return str(partition_number)
    
    def _wordCount(self, key, value):
        for word in value.split(" "):
            value = 1
            partion_name = self.partition(word)
            self.file_write(self.path + "\\P" + partion_name, word + " " + str(value))
                
    def _invertedIndex(self, key, value):
        for line in value:
            for word in line.split(" "):
                partition_name = self.partition(word)
                self.file_write(self.path + "\\P" + partition_name, word + " " + str(key))
        
    
    def map(self, request, context):
        self.n_reducers = request.n_reducers
        self.query = request.query
        
        if request.query == 1:
            for file_name in request.input_split_files:
                file_content = self.file_read(request.input_location + "\\" + file_name)
                for line in range(len(file_content)):
                    response = self._wordCount(line, file_content[line])
        
        elif request.query == 2:
            for file_name in range(len(request.input_split_files)):
                file_content = self.file_read(request.input_location + "\\" + request.input_split_files[file_name])
                response = self._invertedIndex(request.input_split_file_id[file_name], file_content)
        

        # TODO(Avishi): Other Function
        return mapper_pb2.MapResponse(intermediate_file_location = self.path, status = mapper_pb2.MapResponse.Status.SUCCESS)


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