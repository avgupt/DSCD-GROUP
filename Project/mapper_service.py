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