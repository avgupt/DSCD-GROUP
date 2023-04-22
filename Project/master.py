from concurrent import futures
import logging

import grpc
import  mapper_service_pb2 as mapper_pb2
import mapper_service_pb2_grpc as mapper_pb2_grpc
import os
import time
import subprocess

class Master:
    def __init__(self, query, input_location, n_mappers, n_reducers, mappers, reducers, output_location):
        self.query = query
        self.input_location = input_location #ex: wordCount\\input
        self.n_mappers = n_mappers
        self.n_reducers = n_reducers
        self.output_location = output_location
        self.mappers = mappers
        self.reducers = reducers

    def input_split(self):
        files = os.listdir(self.input_location)
        print("input files: ", files)
        n_input_files = len(files)
        mapper_to_files_mapping = {}  # dict of the form {mapper_number: [input1.txt]}
        chunk_size = n_input_files // self.n_mappers
        mapper_i = 1
        file_i = 0

        # first assigning chunk size number of files to each mapper
        while(mapper_i <= self.n_mappers):
            end = file_i + chunk_size
            file_list = []
            while(file_i<end):
                file_list.append(files[file_i])
                file_i = file_i + 1
            mapper_to_files_mapping[mapper_i] = file_list
            mapper_i  = mapper_i + 1

        # assignig remaining files (1 to each mapper)
        mapper_i = 1
        while(file_i < n_input_files):
            mapper_to_files_mapping[mapper_i].append(files[file_i])
            file_i = file_i + 1
            mapper_i = mapper_i + 1
        return mapper_to_files_mapping
    
    def spawn_mappers(self, mappers):
        mappers_process = []
        for mapper_name, port in mappers.items():
            mapper = subprocess.Popen(['python', 'mapper_service.py', str(port), mapper_name])
            print("mapper pid", mapper.pid)
            mappers_process.append(mapper)
            time.sleep(1)
        return mappers_process

    def terminate_mappers(self, mappers_process):
        print("Terminating mappers...")
        for mapper in mappers_process:
            mapper.terminate()

    
    def map(self, mapper_to_files_mapping):
        print(mapper_to_files_mapping[1])
        num = 1
        for mapper_name, port in self.mappers.items():
            with grpc.insecure_channel('localhost:' + str(port), options=(('grpc.enable_http_proxy', 0),)) as channel:
                stub = mapper_pb2_grpc.MapperServiceStub(channel)
                response = stub.map(mapper_pb2.MapRequest(query=self.query, input_location=self.input_location, input_split_files=mapper_to_files_mapping[num]))
                
                if response.status == mapper_pb2.MapResponse.Status.SUCCESS:
                    print("Status : SUCCESS")
                    print("Location of Intermediate data :", response.intermediate_file_location)
                
                else:
                    print("Status : FAILURE")
              
            num += 1



if __name__ == '__main__':
    logging.basicConfig()

    query = int(input("Enter query to perform WordCount[1], InvertedIndex[2], NaturalJoin[3]: ")) # valid input should be given
    input_location = input("Enter input data location(folder name example: 'wordCount\\input'): ")
    output_location = input("Enter output data location(folder name example: 'wordCount\\output'): ")
    n_mappers = int(input("Enter M (no of mappers): "))
    mappers = input("Enter ports of mappers separated by space (eg. 8080 8081 8082):").split()
    n_reducers = int(input("Enter R (no of reducers): "))
    reducers = input("Enter ports of reducers separated by space (eg. 8080 8081 8082):").split()

    # query = 1
    # input_location = 'wordCount\input'
    # output_location = 'wordCount\output'
    # n_mappers = 2
    # mappers = [8084, 8085]
    # n_reducers = 2
    # reducers = [8086, 8087]

    mappers_new = {}
    m = 1
    for port in mappers:
        mapper_name = 'mapper_' + str(m)
        mappers_new[mapper_name] = port
        m = m + 1

    reducers_new = {}
    r = 1
    for port in reducers:
        reducer_name = 'reducer_' + str(r)
        reducers_new[reducer_name] = port
        r = r + 1

    master = Master(query, input_location, n_mappers, n_reducers, mappers_new, reducers_new, output_location)
    mappers_process = master.spawn_mappers(mappers_new)
    mapper_to_files_mapping = master.input_split()
    # print(mapper_to_files_mapping)
    master.map(mapper_to_files_mapping)
    master.terminate_mappers(mappers_process)