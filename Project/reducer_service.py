from concurrent import futures

import grpc
import  reducer_service_pb2 as reducer_pb2
import reducer_service_pb2_grpc as reducer_pb2_grpc

from pathlib import Path
import datetime
import os
import sys

class ReducerServiceServicer(reducer_pb2_grpc.ReducerServiceServicer):
    def __init__(self, reducer_name):
        self.reducer_name = reducer_name
        self.shuffled_and_sorted_data = {}
        self.path = ""
    
    def file_write(self, path, content):
        with open(path, "a+") as file:
            file.write(content + "\n")
    
    def wordCount_reduce_function(self, key, values):
        count = len(values)
        final_output_path = self.path + "\\" + self.reducer_name
        self.file_write(final_output_path , key + " " + str(count))
        return final_output_path
    
    def _wordCount(self, partition_files_path):
        self.shuffled_and_sorted_data = {}
        for file_path in partition_files_path:
            with open(file_path, "r") as file:
                for line in file:
                    data = line.split()
                    key = data[0]
                    value = int(data[1])
                    if key in self.shuffled_and_sorted_data:
                        self.shuffled_and_sorted_data[key].append(value)
                    else:
                        self.shuffled_and_sorted_data[key] = [value]

        for key, value in self.shuffled_and_sorted_data.items():
            final_output_path = self.wordCount_reduce_function(key, value)

        return reducer_pb2.ReduceResponse(status=reducer_pb2.ReduceResponse.Status.SUCCESS, output_file_path=final_output_path)
            


    def reduce(self, request, context):
        self.path = request.output_location
        Path(self.path).mkdir(parents=True, exist_ok=True)
        if request.query == 1:
            return self._wordCount(request.partition_files_path)
        
        # TODO(Avishi): Other Function

class Reducer:

    def __init__(self, port, reducer_name):
        self.address = "localhost"
        self.port = port                        # str
        self.reducer_name = reducer_name
    
    def serve(self, reducer_name):

        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        reducer_pb2_grpc.add_ReducerServiceServicer_to_server(
            ReducerServiceServicer(reducer_name), server
        )
        server.add_insecure_port("[::]:" + self.port)
        server.start()
        server.wait_for_termination()

if __name__ == "__main__":
    # port = input("Enter port for server: ")
    port = sys.argv[1]
    reducer_name = sys.argv[2]
    myServer = Reducer(port, reducer_name)
    myServer.serve(reducer_name)