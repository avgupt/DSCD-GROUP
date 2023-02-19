from __future__ import print_function

import zmq
import uuid

from protos.Article.Article_pb2 import Article, Date
import server_service_pb2 as server_pb2


import logging
import registry_server_service_pb2 as registry_server_service_pb2



class Client:

    def __init__(self):
        uuid_string = str(uuid.uuid1())
        self.id = uuid_string
        

    # RPC from client to Registry server
    def getServerListFromRegistryServer(self):
        request = registry_server_service_pb2.GetServerListRequest(client_uuid=self.id).SerializeToString()
        context = zmq.Context()
        client = context.socket(zmq.REQ)
        client.connect("tcp://localhost:50051")
        client.send(request)
        message = client.recv_multipart()
        response = registry_server_service_pb2.GetServerListResponse()
        response.ParseFromString(message[-1])
        print(response)
        return response

    # We have the server_address using the name of the server. 
    def connectToServer(self, server_name):
        server_list = self.getServerListFromRegistryServer().servers
        server_address = server_list[server_name]
        request = server_pb2.ServerJoinRequest(client_uuid=self.id, fname="connectToServer").SerializeToString()
        context = zmq.Context()
        client = context.socket(zmq.REQ)
        print(server_address)
        client.connect("tcp://"+server_address)
        client.send(request)
        message = client.recv_multipart()
        response = server_pb2.ServerJoinResponse()
        response.ParseFromString(message[-1])
        if response.status == registry_server_service_pb2.Status.SUCCESS:
            print("SUCCESS")
            return True
        
        print("FAIL")
        return False
        

    def leaveServer(self, server_name):
        server_list = self.getServerListFromRegistryServer().servers
        server_address = server_list[server_name]
        request = server_pb2.ServerLeaveRequest(client_uuid=self.id, fname="leaveServer").SerializeToString()
        context = zmq.Context()
        client = context.socket(zmq.REQ)
        client.connect("tcp://"+server_address)
        client.send(request)
        message = client.recv_multipart()
        response = server_pb2.ServerLeaveResponse()
        response.ParseFromString(message[-1])
        if response.status == registry_server_service_pb2.Status.SUCCESS:
            print("SUCCESS")
            return True
        
        print("FAIL")
        return False
        

    def publishArticle(self, sample_article, server_name):
        server_list = self.getServerListFromRegistryServer().servers
        server_address = server_list[server_name]
        request = server_pb2.PublishArticleRequest(client_uuid=self.id, article=sample_article, fname="publishArticle").SerializeToString()
        context = zmq.Context()
        client = context.socket(zmq.REQ)
        client.connect("tcp://"+server_address)
        client.send(request)
        message = client.recv_multipart()
        response = server_pb2.PublishArticleResponse()
        response.ParseFromString(message[-1])
        if response.status == registry_server_service_pb2.Status.SUCCESS:
            print("SUCCESS")
            return True
        
        print("FAIL")
        return False
    
    def getArticles(self, server_name ,date=None, type=None, author=None):
        server_list = self.getServerListFromRegistryServer().servers
        server_address = server_list[server_name]
        request = server_pb2.GetArticlesRequest(client_uuid=self.id, date=date,type=type,author=author, fname="getArticles").SerializeToString()
        context = zmq.Context()
        client = context.socket(zmq.REQ)
        client.connect("tcp://"+server_address)
        client.send(request)
        message = client.recv_multipart()
        response = server_pb2.GetArticlesResponse()
        response.ParseFromString(message[-1])
        print(response)


if __name__ == "__main__":
    sample_date_1 = Date(date=1, month=1, year=2023)
    sample_article_1 = Article(id=1, author="Jane", content="hello world")
    sample_article_2 = Article(id=2, author="John", content="hello world 2")
    myClient = Client()

    while(True):
        print("GetServerList[1], JoinServer[2], LeaveServer[3], GetArticles[4], PublishArticle[5]:")
        n = int(input())

        if n == 1:
            print(myClient.getServerListFromRegistryServer())

        else:
            port = input("Enter server name: ")

            if n == 2:
                print(myClient.connectToServer(port))
            
            elif n == 3:
                print(myClient.leaveServer(port))
            
            elif n == 4:
                # TODO: take input
                print(myClient.getArticles(port, date = sample_date_1))
            
            else:
                article = sample_article_1
                print(myClient.publishArticle(article, port))
