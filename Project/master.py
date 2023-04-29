from concurrent import futures
import logging

import grpc
import  mapper_service_pb2 as mapper_pb2
import mapper_service_pb2_grpc as mapper_pb2_grpc
import  reducer_service_pb2 as reducer_pb2
import reducer_service_pb2_grpc as reducer_pb2_grpc
import os
import time
import subprocess
# import pathlib
import shutil, time
from pathlib import Path
from multiprocessing.pool import ThreadPool

map_intermediate_location = []

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
        mapper_to_files_mapping = {}  # dict of the form {mapper_number: ([input1.txt], 1)}
        chunk_size = n_input_files // self.n_mappers
        mapper_i = 1
        file_i = 0

        if self.query == 3:
            chunk_size = 2
        
        idle_mapper_num = 0
        # first assigning chunk size number of files to each mapper
        while(mapper_i <= self.n_mappers):
            end = file_i + chunk_size
            file_list = []
            file_id_list = []
            while(file_i < end and file_i < n_input_files):
                file_list.append(files[file_i])
                file_id_list.append(file_i)
                file_i = file_i + 1
            if len(file_list) != 0:
                mapper_to_files_mapping[mapper_i] = [file_list, file_id_list]
            else:
                idle_mapper_num += 1
                del self.mappers["mapper_" + str(mapper_i)]
            mapper_i  = mapper_i + 1

        self.n_mappers -= idle_mapper_num
        # assignig remaining files (1 to each mapper)
        mapper_i = 1
        while(file_i < n_input_files):
            mapper_to_files_mapping[mapper_i][0].append(files[file_i])
            mapper_to_files_mapping[mapper_i][1].append(file_i)
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
    
    def spawn_reducers(self, reducers):
        reducers_process = []
        for reducer_name, port in reducers.items():
            reducer = subprocess.Popen(['python', 'reducer_service.py', str(port), reducer_name])
            print("reducer pid", reducer.pid)
            reducers_process.append(reducer)
            time.sleep(1)
        return reducers_process

    def terminate_mappers(self, mappers_process):
        print("Terminating mappers...")
        for mapper in mappers_process:
            mapper.terminate()
    
    def terminate_reducers(self, reducers_process):
        print("Terminating reducers...")
        for reducer in reducers_process:
            reducer.terminate()

    def mapFunction(self, mapper_to_files_mapping, item):
        num = list(self.mappers.items()).index(item) + 1
        port = item[1]
        with grpc.insecure_channel('localhost:' + str(port), options=(('grpc.enable_http_proxy', 0),)) as channel:
                stub = mapper_pb2_grpc.MapperServiceStub(channel)
                response = stub.map(mapper_pb2.MapRequest(query=self.query, input_location=self.input_location, input_split_files=mapper_to_files_mapping[num][0], input_split_file_id=mapper_to_files_mapping[num][1], n_reducers=self.n_reducers))
                
                if response.status == mapper_pb2.MapResponse.Status.SUCCESS:
                    print("Status : SUCCESS")
                    print("Location of Intermediate data :", response.intermediate_file_location)
                    map_intermediate_location.append(response.intermediate_file_location)
                
                else:
                    print("Status : FAILURE")
        

    def reduceFunction(self, intermediate_file_locations, item):
        num = list(self.reducers.items()).index(item) + 1
        port = item[1]
        partition = num - 1
        partition_paths = []
        for path in intermediate_file_locations:
            partition_file_path = path + "/P" + str(partition)
            partition_paths.append(partition_file_path)
        
        with grpc.insecure_channel('localhost:' + str(port), options=(('grpc.enable_http_proxy', 0),)) as channel:
            stub = reducer_pb2_grpc.ReducerServiceStub(channel)
            response = stub.reduce(reducer_pb2.ReduceRequest(query=self.query, partition_files_path=partition_paths, output_location=self.output_location))
            
            if response.status == reducer_pb2.ReduceResponse.Status.SUCCESS:
                print("Status : SUCCESS")
                print("Location of Output data :", response.output_file_path)
            
            else:
                print("Status : FAILURE")
        
    def map(self, mapper_to_files_mapping):
        # print(mapper_to_files_mapping[1])
        input_array = []
        for i in range(len(list(self.mappers.items()))):
            input_array.append((mapper_to_files_mapping, list(self.mappers.items())[i]))

        with ThreadPool() as pool:
            pool.starmap(self.mapFunction, input_array)
        
    def reduce(self, intermediate_file_locations):
        input_array = []
        for i in range(len(list(self.reducers.items()))):
            input_array.append((intermediate_file_locations, list(self.reducers.items())[i]))
        
        with ThreadPool() as pool:
            pool.starmap(self.reduceFunction, input_array)


if __name__ == '__main__':
    logging.basicConfig()

    # query = int(input("Enter query to perform WordCount[1], InvertedIndex[2], NaturalJoin[3]: ")) # valid input should be given
    # input_location = input("Enter input data location(folder name example: 'wordCount/input'): ")
    # output_location = input("Enter output data location(folder name example: 'output'): ")
    # n_mappers = int(input("Enter M (no of mappers): "))
    # mappers = input("Enter ports of mappers separated by space (eg. 8080 8081 8082):").split()
    # n_reducers = int(input("Enter R (no of reducers): "))
    # reducers = input("Enter ports of reducers separated by space (eg. 8080 8081 8082):").split()

    # Delete folder and output
    if Path("folders").exists():
        shutil.rmtree("folders")
    
    if Path("output").exists():
        shutil.rmtree("output")

    query = 2
    input_location = 'invertedIndex/input'
    output_location = 'output'
    n_mappers = 4
    mappers = [8085, 8086, 8087, 8088]
    n_reducers = 2
    reducers = [8810, 8811]

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

    master.map(mapper_to_files_mapping)
    time.sleep(20)
    master.terminate_mappers(mappers_process)

    # print(map_intermediate_location)

    reducers_process = master.spawn_reducers(reducers_new)
    master.reduce(map_intermediate_location)
    time.sleep(20)
    master.terminate_reducers(reducers_process)