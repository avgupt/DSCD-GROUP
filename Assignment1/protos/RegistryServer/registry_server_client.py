from __future__ import print_function

import logging

import grpc
import RegistryServer_pb2
import RegistryServer_pb2_grpc


def run():
    # NOTE(gRPC Python Team): .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs
    # of the code.
    print("Will try to register to registry server ...")
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = RegistryServer_pb2_grpc.RegistryServerServiceStub(channel)
        
        response = stub.RegisterServer(RegistryServer_pb2.RegisterServerRequest(server_name='yoyo'))
    print("Registry Server client received: " + str(response.status))


if __name__ == '__main__':
    logging.basicConfig()
    run()