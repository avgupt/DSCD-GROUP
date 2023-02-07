# //TODO: this file is for demo for grpc client, move it to proper directory
from __future__ import print_function

import logging
import registry_server_service_pb2 
import registry_server_service_pb2_grpc
import grpc


def run():
    # NOTE(gRPC Python Team): .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs
    # of the code.
    print("Will try to register to registry server ...")
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = registry_server_service_pb2_grpc.RegistryServerServiceStub(channel)
        
        response = stub.RegisterServer(registry_server_service_pb2 .RegisterServerRequest(server_name='yoyo'))
    print("Registry Server client received: " + str(response.status))


if __name__ == '__main__':
    logging.basicConfig()
    run()