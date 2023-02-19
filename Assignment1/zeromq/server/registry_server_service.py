from concurrent import futures
import logging

import registry_server_service_pb2 as registry_server_service_pb2 
import zmq
import signal
import time


max_servers = 10
servers = {}

class RegisterServer:

    def start(self, port):    
        context = zmq.Context()
        server = context.socket(zmq.REP)
        server.bind("tcp://*:%s" % port)

        while True:
            message = server.recv_multipart()
            m2 = message[-1].decode("cp437") 
            
            if "localhost" in m2:
                request = registry_server_service_pb2.RegisterServerRequest()
                request.ParseFromString(message[-1])
                server.send(self.RegisterServer(request))
            
            else:
                request = registry_server_service_pb2.GetServerListRequest()
                request.ParseFromString(message[-1])
                server.send(self.GetServerList(request))
            

    def RegisterServer(self, request):
        # Assuming server_name would be unique, otherwise it can override servers map
        server_name = request.server_name
        ip = request.ip
        port = request.port
        address = ip + ':'+ str(port)
        print("JOIN REQUEST FROM", address)
        if len(servers) < max_servers:
            servers[server_name] = address
            print("Server registered to RegistryServer, server name:",server_name)
            return registry_server_service_pb2.RegisterServerResponse(status=registry_server_service_pb2.Status.SUCCESS).SerializeToString()
        return registry_server_service_pb2.RegisterServerResponse(status=registry_server_service_pb2.Status.FAILED).SerializeToString()

    def GetServerList(self, request):
        print("SERVICE LIST REQUEST FROM", request.client_uuid)
        return registry_server_service_pb2.GetServerListResponse(servers=servers).SerializeToString()


def serve():
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    port = '50051'
    server = RegisterServer()
    print("Registry Server started, listening on " + port)
    server.start(port)
    
    

if __name__ == '__main__':
    serve()