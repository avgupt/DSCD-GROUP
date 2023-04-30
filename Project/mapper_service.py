from concurrent import futures

import grpc
import  mapper_service_pb2 as mapper_pb2
import mapper_service_pb2_grpc as mapper_pb2_grpc

from pathlib import Path
import datetime
import os
import pandas as pd
import sys

class MapperServiceServicer(mapper_pb2_grpc.MapperServiceServicer):
    def __init__(self, mapper_name):
        self.mapper_name = mapper_name
        self.path = "folders/" + "ID_" + mapper_name
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
        return str(len(key)%(self.n_reducers))
    
    def _wordCount(self, key, value):
        for word in value.split(" "):
            value = 1
            partion_name = self.partition(word)
            self.file_write(self.path + "/P" + partion_name, word.lower() + " " + str(value))
                
    def _invertedIndex(self, key, value):
        for line in value:
            for word in line.split(" "):
                partition_name = self.partition(word)
                self.file_write(self.path + "/P" + partition_name, word.lower() + " " + str(key))
        
    def _naturalJoinMapCreator(self, table, common_column):
        a, b = [], []
        table.sort_values(common_column)
        col_name = ""
        for col in table.columns:
            if col == common_column:
                a = list(table[col])
            else:
                col_name = col
                b = list(table[col])
        return dict(zip(a, b)), col_name

    def _naturalJoin(self, map1, map2, col_names):
        intersection = {}
        for i in range(self.n_reducers):
            self.file_write(self.path + "/P" + str(i), " ".join(col_names))
        
        for key in map1:
            if key in map2:
                intersection[key] = [[1, map1[key]], [2, map2[key]]]
            else:
                intersection[key] = [[1, map1[key]]]
        for key in map2:
            if key not in intersection:
                intersection[key] = [[2, map2[key]]]

        for key in intersection:
            partition_name = self.partition(key)
            list_str = str()
            for val in intersection[key]:
                list_str += str(val[0]) + " " + str(val[1]) + " "
            self.file_write(self.path + "/P" + str(partition_name), key + " " + list_str)
        return intersection

    def map(self, request, context):
        self.n_reducers = request.n_reducers
        self.query = request.query
        
        if request.query == 1:
            for file_name in request.input_split_files:
                file_content = self.file_read(request.input_location + "/" + file_name)
                for line in range(len(file_content)):
                    response = self._wordCount(line, file_content[line])
        
        elif request.query == 2:
            for file_name in range(len(request.input_split_files)):
                file_content = self.file_read(request.input_location + "/" + request.input_split_files[file_name])
                response = self._invertedIndex(request.input_split_file_id[file_name], file_content)
        
        elif request.query == 3:
            file_names = sorted(request.input_split_files)
            # Assumption1: Two tables and two columns for input
            # Assumption2: One column name is common
            table1 = pd.read_csv(request.input_location + "/" + file_names[0], sep=", ", engine='python')
            table2 = pd.read_csv(request.input_location + "/" + file_names[1], sep=", ", engine='python')
            common_column = list(table2.columns.intersection(table1.columns))[0]
            table1_map, table1_col = self._naturalJoinMapCreator(table1, common_column)
            table2_map, table2_col = self._naturalJoinMapCreator(table2, common_column)
            response = self._naturalJoin(table1_map, table2_map, [common_column, table1_col, table2_col])

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