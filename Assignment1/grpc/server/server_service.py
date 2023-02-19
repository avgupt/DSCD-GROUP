from concurrent import futures
from datetime import date
import logging
import datetime

import grpc
import  server_service_pb2 as server_pb2
import server_service_pb2_grpc as server_pb2_grpc
import registry_server_service_pb2 as registry_server_service_pb2
import registry_server_service_pb2_grpc as registry_server_service_pb2_grpc
from protos.Article.Article_pb2 import Article, Date
from client_client import Client 

hosted_articles = []
hosted_articles_ids = []
clients_server = [] #clients which are server also
clientele = []
max_clients = 10

class ClientServerServicer(server_pb2_grpc.ClientServerServicer):
    def __init__(self, server_name):
        self.name = server_name

    def compareTime(self,article_time, request_articles_time):
        article_date_object = datetime.datetime(article_time.year, article_time.month, article_time.date) # date in yyyy/mm/dd format
        request_articles_date_object = datetime.datetime(request_articles_time.year, request_articles_time.month, request_articles_time.date)
        return article_date_object >= request_articles_date_object

    def filterArticles1(self, time):
        filtered = []
        for article in hosted_articles:
            if self.compareTime(article.time, time):
                filtered.append(article)
        return filtered
    
    def filterArticles2(self, time, author):
        filtered = []
        for article in hosted_articles:
            if self.compareTime(article.time, time) and article.author == author:
                filtered.append(article)
        return filtered

    def filterArticles3(self, time, author, article_type):
        filtered = []
        for article in hosted_articles:
            if self.compareTime(article.time, time) and article.author == author and article.WhichOneof('config') == article_type:
                filtered.append(article)
        return filtered        

    def GetArticles(self, request, context):
        # Assuming a valid request
        print('ARTICLES REQUEST FROM', request.client_uuid)

        filtered = []
        if request.client_uuid not in clientele:
            return server_pb2.GetArticlesResponse(article_list=filtered)

        if request.date and request.author and request.type:
            filtered = self.filterArticles3(request.date, request.author, request.type)
        elif request.date and request.author:
            filtered = self.filterArticles2(request.date, request.author)
        else:
            filtered = self.filterArticles1(request.date)

        return server_pb2.GetArticlesResponse(article_list=filtered)
    
    def PublishArticle(self, request, context):
        print('ARTICLES PUBLISH FROM', request.client_uuid)
        if (request.client_uuid not in clientele) or (request.article.id in hosted_articles_ids):
            # context.cancel()
            return server_pb2.PublishArticleResponse(status=server_pb2.PublishArticleResponse.Status.FAILED)
        print("article request",str(request.article))
        today_date = date.today()
        date_object = Date(date=int(today_date.day), month=int(today_date.month),year=int(today_date.year))
        print(date_object)
        article =  Article(id=request.article.id, author=request.article.author, time=date_object, content=request.article.content)
        hosted_articles.append(article)
        hosted_articles_ids.append(request.article.id)
        print(hosted_articles)

        # (BONUS) add published article to client_server hosted_articles
        for client_server_name in clients_server:
            self.publishArticleToJoinedServer(client_server_name,article)

        return server_pb2.PublishArticleResponse(status=server_pb2.PublishArticleResponse.Status.SUCCESS)

    # (BONUS)
    def publishArticleToJoinedServer(self,client_server_name,article):
        myClient = Client(server_name=self.name)
        myClient.connectToServer(client_server_name)
        myClient.publishArticle(sample_article=article,server_name=client_server_name)
        myClient.leaveServer(client_server_name)


    def JoinServer(self, request, context):
        # Assuming unique UUID for client.
        client_uuid = request.client_uuid
        print('JOIN REQUEST FROM', client_uuid)
        
        if len(clientele) < max_clients:
            # if client requesting to join is a server then add its uuid to clients_server (BONUS)
            if request.is_server and (client_uuid not in clients_server):
                clients_server.append(client_uuid)
            clientele.append(client_uuid)
            # Success: client accepted and added to clientale.
            return server_pb2.ServerJoinResponse(status=server_pb2.ServerJoinResponse.Status.SUCCESS)
        
        # Failure: Client not added to the clientale list
        return server_pb2.ServerJoinResponse(status=server_pb2.ServerJoinResponse.Status.FAILED)
    
    def LeaveServer(self, request, context):
        # Assuming unique UUID for client
        client_uuid = request.client_uuid
        print("LEAVE REQUEST FROM", client_uuid)
        
        if (client_uuid in clientele):
            clientele.remove(client_uuid)
            if (client_uuid in clients_server):
                clients_server.remove(client_uuid)
            return server_pb2.ServerLeaveResponse(status=server_pb2.ServerLeaveResponse.Status.SUCCESS)

        return server_pb2.ServerLeaveResponse(status=server_pb2.ServerLeaveResponse.Status.FAILED)



class Server:

    def __init__(self, port,server_name):
        self.address = "localhost"
        self.port = port                        # str
        self.hosted_articles = []               # Article[]
        self.clients_server = []                   # Client[]
        self.clientele = []                     # Client[]

        self.name = server_name

    def start(self):
        if not self.__isRegistered():
            print("Could not register server")
        else:
            self.__serve()

    def __isRegistered(self)->bool:
        # TODO(guptashelly): call Register RPC and return response
        print("Will try to register to registry server ...")
        with grpc.insecure_channel('localhost:50051') as channel:
            stub = registry_server_service_pb2_grpc.RegistryServerServiceStub(channel)
            
            response = stub.RegisterServer(registry_server_service_pb2.RegisterServerRequest(server_name=self.name,ip=self.address,port=int(self.port)))
        print(response.status)
        print("Registry Server client received: " + str(response.status))
        return response.status
    
    def __serve(self):
        # TODO(avishi): Refactor code // Remove plag
        # Reference: https://realpython.com/python-microservices-grpc/

        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        server_pb2_grpc.add_ClientServerServicer_to_server(
            ClientServerServicer(self.name), server
        )
        server.add_insecure_port("[::]:" + self.port)
        server.start()
        server.wait_for_termination()

if __name__ == "__main__":
    port = input("Enter port for server: ")
    server_name = input("Enter server name: ")

    myServer = Server(port,server_name)
    myServer.start()
