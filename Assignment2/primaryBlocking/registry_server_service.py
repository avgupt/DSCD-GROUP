from concurrent import futures
import logging

import grpc
import registry_server_service_pb2 as registry_server_service_pb2 
import registry_server_service_pb2_grpc as registry_server_service_pb2_grpc



class RegisterService(registry_server_service_pb2_grpc.RegistryServerServiceServicer):
    servers = {}
    primary_replica_ip = ""
    primary_replica_port = ""

    def RegisterReplica(self, request, context):
        # Assuming replica_name would be unique, otherwise it can override servers map
        replica_name = request.replica_name
        ip = request.ip
        port = request.port
        address = ip + ':'+ str(port)
        print("JOIN REQUEST FROM", address)
        is_primary_replica = False
        if len(self.servers) == 0:
            is_primary_replica = True
            self.primary_replica_ip = ip
            self.primary_replica_port = port

        self.servers[replica_name] = address
        print("Replica registered to RegistryServer, replica name:",replica_name)
        return registry_server_service_pb2.RegisterReplicaResponse(is_replica_primary = is_primary_replica, primary_replica_ip = self.primary_replica_ip, primary_replica_port = self.primary_replica_port)
    
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