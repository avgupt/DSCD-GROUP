from __future__ import print_function

import grpc
import uuid

from protos.Article.Article_pb2 import Article, Date
import server_service_pb2 as server_pb2
import server_service_pb2_grpc as server_pb2_grpc


import logging
import registry_server_service_pb2 as registry_server_service_pb2
import registry_server_service_pb2_grpc as registry_server_service_pb2_grpc



class Client:

    def __init__(self):
        uuid_string = str(uuid.uuid1())
        self.id = uuid_string
        

    # RPC from client to Registry server
    def getServerListFromRegistryServer(self):
        with grpc.insecure_channel('localhost:50051') as channel:
            stub = registry_server_service_pb2_grpc.RegistryServerServiceStub(channel)
            response = stub.GetServerList(registry_server_service_pb2.GetServerListRequest())
            print(response)
            channel.close()
            return response

    # We have the server_address using the name of the server. 
    def connectToServer(self, server_name):
        server_list = self.getServerListFromRegistryServer().servers
        server_address = server_list[server_name]
        with grpc.insecure_channel(server_address) as channel:
            stub = server_pb2_grpc.ClientServerStub(channel)
            response = stub.JoinServer(server_pb2.ServerJoinRequest(client_uuid=self.id))
            print(response)
            channel.close()

    def leaveServer(self, server_name):
        server_list = self.getServerListFromRegistryServer().servers
        server_address = server_list[server_name]
        with grpc.insecure_channel(server_address) as channel:
            stub = server_pb2_grpc.ClientServerStub(channel)
            response = stub.LeaveServer(server_pb2.ServerLeaveRequest(client_uuid=self.id))
            print(response.status)
            channel.close()

    def publishArticle(self, sample_article, server_name):
        server_list = self.getServerListFromRegistryServer().servers
        server_address = server_list[server_name]
        
        with grpc.insecure_channel(server_address , options=(('grpc.enable_http_proxy', 0),)) as channel:
            stub = server_pb2_grpc.ClientServerStub(channel)
            response = stub.PublishArticle(server_pb2.PublishArticleRequest(client_uuid=self.id, article=sample_article))
            print(response.status)
            channel.close()
    
    def getArticles(self, server_name ,date=None, type=None, author=None):
        server_list = self.getServerListFromRegistryServer().servers
        server_address = server_list[server_name]
        
        with grpc.insecure_channel(server_address , options=(('grpc.enable_http_proxy', 0),)) as channel:
            stub = server_pb2_grpc.ClientServerStub(channel)       
            response = stub.GetArticles(server_pb2.GetArticlesRequest(client_uuid=self.id,date=date,type=type,author=author))
            print(response)
            channel.close()

    # def start(self, server_address):
    #     # TODO(avishi): Refactor code
    #     # Reference: www.tutorialspoint.com/grpc/grpc_helloworld_app_with_python.htm
    #     print(self.id)
    #     with grpc.insecure_channel(server_address , options=(('grpc.enable_http_proxy', 0),)) as channel:
    #         stub = server_pb2_grpc.ClientServerStub(channel)
    #         # response = stub.PublishArticle(server_pb2.PublishArticleRequest(client_uuid=self.id, article=sample_article_1))
    #         # print(response)
    #         # response = stub.PublishArticle(server_pb2.PublishArticleRequest(client_uuid=self.id, article=sample_article_2))
    #         # # print(response)
    #         response = stub.GetArticles(server_pb2.GetArticlesRequest(client_uuid=self.id))
    #         print(response)
    #         # response = stub.PublishArticle(server_pb2.PublishArticleRequest(client_uuid=self.id, article=sample_article_3))
    #         # response = stub.GetArticles(server_pb2.GetArticlesRequest(client_uuid=self.id, date=sample_date_1))
    #         # print(response)
    #         channel.close()

