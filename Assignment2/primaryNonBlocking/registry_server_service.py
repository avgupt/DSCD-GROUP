from concurrent import futures
import logging

import grpc
import  server_service_pb2 as server_pb2
import server_service_pb2_grpc as server_pb2_grpc
import registry_server_service_pb2 as registry_server_service_pb2 
import registry_server_service_pb2_grpc as registry_server_service_pb2_grpc



class RegisterService(registry_server_service_pb2_grpc.RegistryServerServiceServicer):
    servers = []
    primary_replica_ip = ""
    primary_replica_port = ""

    def RegisterReplica(self, request, context):
        ip = request.ip
        port = request.port
        address = ip + ':'+ str(port)
        print("JOIN REQUEST FROM", address)
        is_primary_replica = False

        if address in self.servers:
            print("Can't register, port already in use:",address)
            return registry_server_service_pb2.RegisterReplicaResponse(is_replica_primary = is_primary_replica, primary_replica_ip = self.primary_replica_ip, primary_replica_port = self.primary_replica_port,status=registry_server_service_pb2.RegisterReplicaResponse.FAILED)

        if len(self.servers) == 0:
            is_primary_replica = True
            self.primary_replica_ip = ip
            self.primary_replica_port = port

        replica_name = 'replica_' + str(len(self.servers))

        if is_primary_replica is False:
            primary_replica_address = self.primary_replica_ip + ':' + str(self.primary_replica_port)
            self.sendReplicaInfoToPrimaryReplica(ip,port,primary_replica_address)
        
        self.servers.append(address)
        print("Replica registered to RegistryServer, replica address:",address)
        return registry_server_service_pb2.RegisterReplicaResponse(is_replica_primary = is_primary_replica, primary_replica_ip = self.primary_replica_ip, primary_replica_port = self.primary_replica_port,replica_name=replica_name,status=registry_server_service_pb2.RegisterReplicaResponse.SUCCESS)
    
    def sendReplicaInfoToPrimaryReplica(self,ip,port,primary_replica_address):
        with grpc.insecure_channel(primary_replica_address , options=(('grpc.enable_http_proxy', 0),)) as channel:
            stub = server_pb2_grpc.ServerServiceStub(channel)      
            response = stub.SendReplicaInfoToPrimary(server_pb2.SendReplicaInfoToPrimaryRequest(ip=ip,port=port))
            print(response.status)
            channel.close()
            return response
        
    def GetReplicaList(self, request, context):
        print("REPLICA LIST REQUEST")
        return registry_server_service_pb2.GetReplicaListResponse(servers=self.servers)


def serve():
    port = '50051'
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    registry_server_service_pb2_grpc.add_RegistryServerServiceServicer_to_server(RegisterService(), server)
    server.add_insecure_port('[::]:' + port)
    server.start()
    print("Registry Server started, listening on " + port)
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    serve()