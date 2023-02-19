from __future__ import print_function

import grpc
import uuid

from protos.Article.Article_pb2 import Article, Date
import server_service_pb2 as server_pb2
import server_service_pb2_grpc as server_pb2_grpc


import logging
import registry_server_service_pb2 as registry_server_service_pb2
import registry_server_service_pb2_grpc as registry_server_service_pb2_grpc

import argparse

class Client:

    def __init__(self,server_name=None):
        uuid_string = str(uuid.uuid1())
        self.client_is_server = server_name is not None
        if server_name is not None:
            self.id = server_name
        else:
            self.id = uuid_string
        

    # RPC from client to Registry server
    def getServerListFromRegistryServer(self):
        with grpc.insecure_channel('localhost:50051') as channel:
            stub = registry_server_service_pb2_grpc.RegistryServerServiceStub(channel)
            response = stub.GetServerList(registry_server_service_pb2.GetServerListRequest(client_uuid=self.id))
            print(response.servers)
            channel.close()
            return response

    # We have the server_address using the name of the server. 
    def connectToServer(self, server_name):
        server_list = self.getServerListFromRegistryServer().servers
        server_address = server_list[server_name]
        if self.client_is_server:
                client_address = server_list[self.id]
                with grpc.insecure_channel(client_address) as channel:
                    stub = server_pb2_grpc.ClientServerStub(channel)
                    response = stub.ClientServerJoinServer(server_pb2.ClientServerJoinServerRequest(server_address=server_address))
                    print(response)
                    channel.close()
        else:
            with grpc.insecure_channel(server_address) as channel:
                stub = server_pb2_grpc.ClientServerStub(channel)
                response = stub.JoinServer(server_pb2.ServerJoinRequest(client_uuid=self.id,is_server=self.client_is_server))
                print(response)
                channel.close()

    def leaveServer(self, server_name):
        server_list = self.getServerListFromRegistryServer().servers
        server_address = server_list[server_name]
        with grpc.insecure_channel(server_address) as channel:
            stub = server_pb2_grpc.ClientServerStub(channel)
            response = stub.LeaveServer(server_pb2.ServerLeaveRequest(client_uuid=self.id))
            print(response)
            channel.close()

    def publishArticle(self, sample_article, server_name):
        server_list = self.getServerListFromRegistryServer().servers
        server_address = server_list[server_name]
        
        with grpc.insecure_channel(server_address , options=(('grpc.enable_http_proxy', 0),)) as channel:
            stub = server_pb2_grpc.ClientServerStub(channel)
            response = stub.PublishArticle(server_pb2.PublishArticleRequest(client_uuid=self.id, article=sample_article))
            print(response)
            channel.close()
    
    def getArticles(self, server_name ,date=None, type=None, author=None):
        server_list = self.getServerListFromRegistryServer().servers
        server_address = server_list[server_name]
        
        with grpc.insecure_channel(server_address , options=(('grpc.enable_http_proxy', 0),)) as channel:
            stub = server_pb2_grpc.ClientServerStub(channel)       
            response = stub.GetArticles(server_pb2.GetArticlesRequest(client_uuid=self.id,date=date,type=type,author=author,visited=[]))

            print(response.article_list)
            channel.close()

if __name__== "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-server", help="Server name")
    args = parser.parse_args()
    server = args.server
    myClient = Client(server_name=server)
