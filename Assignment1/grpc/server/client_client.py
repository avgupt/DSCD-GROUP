from __future__ import print_function

import grpc
import uuid

from protos.Article.Article_pb2 import Article, Date
import server_service_pb2 as server_pb2
import server_service_pb2_grpc as server_pb2_grpc


import logging
import registry_server_service_pb2 as registry_server_service_pb2
import registry_server_service_pb2_grpc as registry_server_service_pb2_grpc


sample_date_1 = Date(date=1, month="January", year=2023)
sample_date_2 = Date(date=8, month="January", year=2023)
sample_date_3 = Date(date=16, month="February", year=2023)
sample_date_4 = Date(date=21, month="March", year=2023)

sample_article_1 = Article(id=1, author="Jane", time=sample_date_1, content="hello world")
sample_article_2 = Article(id=2, author="John", time=sample_date_2, content="hello world1")
sample_article_3 = Article(id=3, author="Jolly", time=sample_date_1, content="hello world2")
sample_article_4 = Article(id=4, author="Jan", time=sample_date_4, content="hello world3")

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
        server_list = self.getServerListFromRegistryServer()
        server_address = server_list[server_name]
        with grpc.insecure_channel(server_address) as channel:
            stub = server_pb2_grpc.ClientServerStub(channel)
            response = stub.LeaveServer(server_pb2.ServerLeaveRequest(client_uuid=self.id))
            print(response)
            channel.close()

    def publishArticle(self, sample_article, server_name):
        server_list = self.getServerListFromRegistryServer()
        server_address = server_list[server_name]
        
        with grpc.insecure_channel(server_address , options=(('grpc.enable_http_proxy', 0),)) as channel:
            stub = server_pb2_grpc.ClientServerStub(channel)
            response = stub.PublishArticle(server_pb2.PublishArticleRequest(client_uuid=self.id, article=sample_article))
            print(response)
            channel.close()
    
    # def getArticles(self, type=None)
        

    def start(self, server_address):
        # TODO(avishi): Refactor code
        # Reference: www.tutorialspoint.com/grpc/grpc_helloworld_app_with_python.htm
        print(self.id)
        with grpc.insecure_channel(server_address , options=(('grpc.enable_http_proxy', 0),)) as channel:
            stub = server_pb2_grpc.ClientServerStub(channel)
            # response = stub.PublishArticle(server_pb2.PublishArticleRequest(client_uuid=self.id, article=sample_article_1))
            # print(response)
            # response = stub.PublishArticle(server_pb2.PublishArticleRequest(client_uuid=self.id, article=sample_article_2))
            # # print(response)
            response = stub.GetArticles(server_pb2.GetArticlesRequest(client_uuid=self.id))
            print(response)
            # response = stub.PublishArticle(server_pb2.PublishArticleRequest(client_uuid=self.id, article=sample_article_3))
            # response = stub.GetArticles(server_pb2.GetArticlesRequest(client_uuid=self.id, date=sample_date_1))
            # print(response)
            channel.close()


if __name__ == "__main__":
    myClient1 = Client()
    # name input - path
    # myClient1.connectToServer('localhost:8080')
    myClient1.connectToServer('server_8080')

    # myClient1.start('localhost:8080')

    # myClient2 = Client()
    # # myClient2.connectToServer('localhost:8080')
    # myClient2.leaveServer('localhost:8080')
