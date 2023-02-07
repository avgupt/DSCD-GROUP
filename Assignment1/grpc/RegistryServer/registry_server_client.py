# //TODO: this file is just for demo for grpc client, move it to proper directory
from __future__ import print_function

import logging
import registry_server_service_pb2 
import registry_server_service_pb2_grpc
import grpc


def run():
    print("Will try to register to registry server ...")
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = registry_server_service_pb2_grpc.RegistryServerServiceStub(channel)
        
        response = stub.RegisterServer(registry_server_service_pb2.RegisterServerRequest(server_name='yoyo1',ip='localhost',port=1000))
        response2 = stub.GetServerList(registry_server_service_pb2.GetServerListRequest())
    print("Registry Server client received: " + str(response.status))
    print(str(response2))


if __name__ == '__main__':
    logging.basicConfig()
    run()