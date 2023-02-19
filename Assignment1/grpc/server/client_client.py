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

sample_date_1 = Date(date=1, month=1, year=2023)
sample_date_2 = Date(date=8, month=1, year=2023)
sample_date_3 = Date(date=16, month=2, year=2023)
sample_date_4 = Date(date=21, month=3, year=2023)

sample_article_1 = Article(id=1, author="Jane", content="hello world", sports="SPORTS")
sample_article_2 = Article(id=1, author="Jane", content="hello world", fashion="FASHION")
sample_article_3 = Article(id=3, author="Jolly", content="hello world2")
sample_article_4 = Article(id=4, author="Jan",  content="hello world3")

ARTICLE_TYPE = {'S': 'sports', 'F': 'fashion', 'P': 'politics'}

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
                    if response.status is server_pb2.ClientServerJoinServerResponse.Status.SUCCESS:
                        print("SUCCESS")
                    else:
                        print("FAILED")
                    channel.close()
        else:
            with grpc.insecure_channel(server_address) as channel:
                stub = server_pb2_grpc.ClientServerStub(channel)
                response = stub.JoinServer(server_pb2.ServerJoinRequest(client_uuid=self.id,is_server=self.client_is_server))
                if response.status is server_pb2.ServerJoinResponse.Status.SUCCESS:
                    print("SUCCESS")
                else:
                    print("FAILED")
                channel.close()

    def leaveServer(self, server_name):
        server_list = self.getServerListFromRegistryServer().servers
        server_address = server_list[server_name]
        with grpc.insecure_channel(server_address) as channel:
            stub = server_pb2_grpc.ClientServerStub(channel)
            response = stub.LeaveServer(server_pb2.ServerLeaveRequest(client_uuid=self.id))
            if response.status is server_pb2.ServerLeaveResponse.Status.SUCCESS:
                print("SUCCESS")
            else:
                print("FAILED")
            channel.close()

    def publishArticle(self, sample_article, server_name):
        server_list = self.getServerListFromRegistryServer().servers
        server_address = server_list[server_name]
        
        with grpc.insecure_channel(server_address , options=(('grpc.enable_http_proxy', 0),)) as channel:
            stub = server_pb2_grpc.ClientServerStub(channel)
            response = stub.PublishArticle(server_pb2.PublishArticleRequest(client_uuid=self.id, article=sample_article))
            if response.status is server_pb2.PublishArticleResponse.Status.SUCCESS:
                print("SUCCESS")
            else:
                print("FAILED")
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

    while(True):
        print("GetServerList[1], JoinServer[2], LeaveServer[3], GetArticles[4], PublishArticle[5]:")
        n = int(input())

        if n == 1:
            myClient.getServerListFromRegistryServer()
        elif n > 5:
            print("INVALID REQUEST")
        else:
            server_name = input("Enter server name: ")

            if n == 2:
                myClient.connectToServer(server_name)
            
            elif n == 3:
                myClient.leaveServer(server_name)
            
            elif n == 4:
                 # # Assuming valid input
                date = input("Enter date (dd/mm/yyyy): ")
                article_type = input("Enter type (Sports(S), fashion(F), politics(P): ")
                author = input("Enter author: ")

                if date != '':
                    date = Date(date=int(date.split("/")[0]), month=int(date.split('/')[1]), year=int(date.split('/')[2]))
                else:
                    date = None
                if article_type in ARTICLE_TYPE.keys():
                    article_type = ARTICLE_TYPE[article_type]
                
                myClient.getArticles(server_name=server_name,date=date,author=author,type=article_type)

            
            else:
                article_num = int(input("Enter article number: "))
                article = sample_article_4
                if article_num == 1:
                    article = sample_article_1
                elif article_num == 2:
                    article = sample_article_2
                elif article == 3:
                    article = sample_article_3
                myClient.publishArticle(article,server_name)
                # articles = myClient.GetArticles(port, date, article_type, author)
