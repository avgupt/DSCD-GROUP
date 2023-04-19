from concurrent import futures
import logging

import grpc
import  mapper_service_pb2 as mapper_pb2
import mapper_service_pb2_grpc as mapper_pb2_grpc
import master_service_pb2 as master_service_pb2 
import master_service_pb2_grpc as master_service_pb2_grpc
import os


class MasterService(master_service_pb2_grpc.MasterServiceServicer):
    def __init__(self, query, n_mappers, n_reducers):
        self.query = query
        self.n_mappers = n_mappers
        self.n_reducers = n_reducers
        self.mappers = []
        self.reducers = []

    def RegisterMapper(self, request, context):
        ip = request.ip
        port = request.port
        address = ip + ':'+ str(port)
        print("JOIN REQUEST FROM", address)

        if len(self.mappers) == self.n_mappers:
            print("Can't register, enough mappers live:",address)
            return master_service_pb2.RegisterMapperResponse(status=master_service_pb2.RegisterMapperResponse.FAILED)

        if address in self.mappers:
            print("Can't register, port already in use:",address)
            return master_service_pb2.RegisterMapperResponse(status=master_service_pb2.RegisterMapperResponse.FAILED)

        mapper_name = 'mapper_' + str(len(self.mappers))
        self.mappers.append(address)
        print("Mapper registered to Master, mapper address:",address)
        return master_service_pb2.RegisterMapperResponse(mapper_name=mapper_name,status=master_service_pb2.RegisterMapperResponse.SUCCESS)


class Master:
    def __init__(self, query, input_location, n_mappers, n_reducers, output_location):
        self.query = query
        self.input_location = input_location #ex: wordCount\\input
        self.n_mappers = n_mappers
        self.n_reducers = n_reducers
        self.output_location = output_location

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

    def serve(self):
        port = '50051'
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        master_service_pb2_grpc.add_MasterServiceServicer_to_server(MasterService(self.query,self.n_mappers,self.n_reducers), server)
        server.add_insecure_port('[::]:' + port)
        server.start()
        print("Master started, listening on " + port)
        server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()

    query = int(input("Enter query to perform WordCount[1], InvertedINdex[2], NaturalJoin[3]: ")) # valid input should be given
    input_location = input("Enter input data location(folder name example: 'wordCount\\input'): ")
    output_location = input("Enter output data location(folder name example: 'wordCount\\output'): ")
    n_mappers = int(input("Enter M (no of mappers): "))
    n_reducers = int(input("Enter R (no of reducers): "))

    master = Master(query, input_location, n_mappers, n_reducers, output_location)
    mapper_to_files_mapping = master.input_split()
    print(mapper_to_files_mapping)
    master.serve()