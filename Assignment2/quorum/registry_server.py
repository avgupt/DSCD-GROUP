from concurrent import futures
import logging, random, sys

import grpc
import protos.registry_server_service_pb2_grpc as registry_server_service_pb2_grpc

from protos.registry_server_service_pb2 import Request, Response
from protos.status_pb2 import Status

servers = []
Nr = 0
Nw = 0
N = 0

class RegistryServerService(registry_server_service_pb2_grpc.RegistryServerServiceServicer):

    def getServers(self, request, context):
        response = servers    
        if request.type == Request.REQUEST_TYPE.READ:
            # randomly select Nr servers
            response = random.sample(servers, k=Nr)
        elif request.type == Request.REQUEST_TYPE.WRITE or request.type == Request.REQUEST_TYPE.DELETE:
            response = random.sample(servers, k=Nw)
        return Response(server_list=response)

    def connect(self, request, context):
        # Assumption: no duplicate servers.
        print("Request received from LOCALHOST:" + request.port)
        servers.append(request)
        return Status(type=Status.STATUS_TYPE.SUCCESS)

    
def is_quorum_valid():
    return Nr + Nw > N and Nw > N / 2

def serve():
    port = '8888'
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    registry_server_service_pb2_grpc.add_RegistryServerServiceServicer_to_server(RegistryServerService(), server)
    server.add_insecure_port('[::]:' + port)
    server.start()
    print("Registry Server started, listening on " + port)
    server.wait_for_termination()


def input_constraints():
    Nr = int(input("Enter Nr: "))
    Nw = int(input("Enter Nw: "))
    N = int(input("Enter N: "))
    return Nr, Nw, N

if __name__ == '__main__':
    # Nr, Nw, N = input_constraints()
    # Nr = int(sys.argv[1])
    # Nw = int(sys.argv[2])
    # N = int(sys.argv[3])

    Nr, Nw, N = 3, 3, 4

    while(not is_quorum_valid()):
        print("ERROR: Enter valid constraints.\n")
        Nr, Nw, N = input_constraints()
    
    print("SUCCESS: Valid constraints.\n")
    logging.basicConfig()
    serve()
