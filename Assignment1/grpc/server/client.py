from __future__ import print_function

import grpc
import uuid

import server_service_pb2 as server_pb2
import server_service_pb2_grpc as server_pb2_grpc

from protos.Article.Article_pb2 import Article, Date

import logging
import RegistryServer.registry_server_service_pb2 as registry_server_service_pb2
import RegistryServer.registry_server_service_pb2_grpc as registry_server_service_pb2_grpc


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
        # self.id = id
        self.id = uuid_string
        self.run()

        # self.start()
    
    def startRegistryServer():
        print("Will try to register to registry server ...")
        with grpc.insecure_channel('localhost:50051') as channel:
            stub = registry_server_service_pb2_grpc.RegistryServerServiceStub(channel)
    
        # response = stub.RegisterServer(registry_server_service_pb2.RegisterServerRequest(server_name='yoyo1',ip='localhost',port=1000))
    

    # We have the server_address using the name of the server. 
    def connectToServer(self, server_address):
        with grpc.insecure_channel(server_address) as channel:
            stub = server_pb2_grpc.ClientServerStub(channel)

            response = stub.JoinServer(server_pb2.ServerJoinRequest(client_uuid=self.id))
            # print("Something", type(response))
            print(response)
            channel.close()

    def leaveServer(self, server_address):
        with grpc.insecure_channel(server_address) as channel:
            stub = server_pb2_grpc.ClientServerStub(channel)

            response = stub.LeaveServer(server_pb2.ServerLeaveRequest(client_uuid=self.id))
            # print("Something", type(response))
            print(response)
            channel.close()

    def start(self, server_address):
        # TODO(avishi): Refactor code
        # Reference: www.tutorialspoint.com/grpc/grpc_helloworld_app_with_python.htm
        print(self.id)
        with grpc.insecure_channel(server_address , options=(('grpc.enable_http_proxy', 0),)) as channel:
            stub = server_pb2_grpc.ClientServerStub(channel)
            response = stub.PublishArticle(server_pb2.PublishArticleRequest(client_uuid=self.id, article=sample_article_1))
            print(response)
            response = stub.PublishArticle(server_pb2.PublishArticleRequest(client_uuid=self.id, article=sample_article_2))
            print(response)
            response = stub.GetArticles(server_pb2.GetArticlesRequest(client_uuid=self.id, date=sample_date_2))
            print(response)
            response = stub.PublishArticle(server_pb2.PublishArticleRequest(client_uuid=self.id, article=sample_article_3))
            response = stub.GetArticles(server_pb2.GetArticlesRequest(client_uuid=self.id, date=sample_date_1))
            print(response)
            channel.close()


if __name__ == "__main__":
    myClient1 = Client()
    # name input - path
    myClient1.connectToServer('localhost:8080')

    myClient1.start('localhost:8080')

    # myClient2 = Client()
    # # myClient2.connectToServer('localhost:8080')
    # myClient2.leaveServer('localhost:8080')
