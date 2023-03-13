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

hosted_articles = []
clientele = []
max_clients = 10
subscribed_to = [] # stores address of servers this server is subscribed to

class ClientServerServicer(server_pb2_grpc.ClientServerServicer):
    def __init__(self, server_name):
        self.name = server_name

    def compareTime(self,article_time, request_articles_time):
        article_date_object = datetime.datetime(article_time.year, article_time.month, article_time.date) # date in yyyy/mm/dd format
        request_articles_date_object = datetime.datetime(request_articles_time.year, request_articles_time.month, request_articles_time.date)
        return article_date_object >= request_articles_date_object

    def filterArticlesTime(self, time):
        filtered = []
        for article in hosted_articles:
            if self.compareTime(article.time, time):
                filtered.append(article)
        return filtered
    
    def filterArticlesAuthorAndTime(self, time, author):
        filtered = []
        for article in hosted_articles:
            if self.compareTime(article.time, time) and article.author == author:
                filtered.append(article)
        return filtered

    def filterArticlesTypeAndTime(self, time, article_type):
        filtered = []
        for article in hosted_articles:
            if self.compareTime(article.time, time) and article.WhichOneof('type') == article_type:
                filtered.append(article)
        return filtered 

    def filterArticlesAuthorAndTimeAndType(self, time, author, article_type):
        filtered = []
        for article in hosted_articles:
            if self.compareTime(article.time, time) and article.author == author and article.WhichOneof('type') == article_type:
                filtered.append(article)
        return filtered        

    def GetArticles(self, request, context):
        # Assuming a valid request
        print('ARTICLES REQUEST FROM', request.client_uuid)

        if self.name in request.visited:
            return server_pb2.GetArticlesResponse(article_list=[])

        visited = request.visited
        visited.append(self.name)

        filtered = []
        if request.client_uuid not in clientele:
            return server_pb2.GetArticlesResponse(article_list=filtered)

        if request.date and request.author and request.type:
            filtered = self.filterArticlesAuthorAndTimeAndType(request.date, request.author, request.type)
        elif request.date and request.author:
            filtered = self.filterArticlesAuthorAndTime(request.date, request.author)
        elif request.date and request.type:
            filtered = self.filterArticlesTypeAndTime(request.date, request.type)
        else:
            filtered = self.filterArticlesTime(request.date)

        for server_address in subscribed_to:
            response = self.getArticlesFromJoinedServer(server_address,visited,request.date,request.author,request.type)
            filtered.extend(response.article_list)
        return server_pb2.GetArticlesResponse(article_list=filtered)

    def getArticlesFromJoinedServer(self,server_address,visited,date=None,type=None,author=None):
        with grpc.insecure_channel(server_address , options=(('grpc.enable_http_proxy', 0),)) as channel:
            stub = server_pb2_grpc.ClientServerStub(channel)       
            response = stub.GetArticles(server_pb2.GetArticlesRequest(client_uuid=self.name,date=date,type=type,author=author,visited=visited))
            print(response.article_list)
            channel.close()
            return response
    
    def PublishArticle(self, request, context):
        print('ARTICLES PUBLISH FROM', request.client_uuid)
        if (request.client_uuid not in clientele):
            return server_pb2.PublishArticleResponse(status=server_pb2.PublishArticleResponse.Status.FAILED)
        today_date = date.today()
        date_object = Date(date=int(today_date.day), month=int(today_date.month),year=int(today_date.year))
        # article =  Article(id=request.article.id, author=request.article.author, time=date_object, content=request.article.content)
        if (request.article.WhichOneof('type') == "sports"):
            article =  Article(id=request.article.id, author=request.article.author, time=date_object, content=request.article.content, sports="SPORTS")
        elif (request.article.WhichOneof('type') == "fashion"):
            article =  Article(id=request.article.id, author=request.article.author, time=date_object, content=request.article.content, fashion="FASHION")
        else:
            article =  Article(id=request.article.id, author=request.article.author, time=date_object, content=request.article.content, politics="POLITICS")
        hosted_articles.append(article)
        return server_pb2.PublishArticleResponse(status=server_pb2.PublishArticleResponse.Status.SUCCESS)

    def JoinServer(self, request, context):
        # Assuming unique UUID for client.
        client_uuid = request.client_uuid
        print('JOIN REQUEST FROM', client_uuid)
        
        if len(clientele) < max_clients:
            clientele.append(client_uuid)
            # Success: client accepted and added to clientale.
            return server_pb2.ServerJoinResponse(status=server_pb2.ServerJoinResponse.Status.SUCCESS)
        
        # Failure: Client not added to the clientale list
        return server_pb2.ServerJoinResponse(status=server_pb2.ServerJoinResponse.Status.FAILED)

    def ClientServerJoinServer(self, request, context):
        with grpc.insecure_channel(request.server_address) as channel:
                stub = server_pb2_grpc.ClientServerStub(channel)
                response = stub.JoinServer(server_pb2.ServerJoinRequest(client_uuid=self.name,is_server=True))
                subscribed_to.append(request.server_address)
                channel.close()
                if response.status is server_pb2.ServerJoinResponse.Status.SUCCESS:
                    return server_pb2.ClientServerJoinServerResponse(status=server_pb2.ClientServerJoinServerResponse.Status.SUCCESS)
        return server_pb2.ClientServerJoinServerResponse(status=server_pb2.ClientServerJoinServerResponse.Status.FAILED)

    
    def LeaveServer(self, request, context):
        # Assuming unique UUID for client
        client_uuid = request.client_uuid
        print("LEAVE REQUEST FROM", client_uuid)
        
        if (client_uuid in clientele):
            clientele.remove(client_uuid)
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
        print("Will try to register to registry server ...")
        with grpc.insecure_channel('localhost:50051') as channel:
            stub = registry_server_service_pb2_grpc.RegistryServerServiceStub(channel)
            
            response = stub.RegisterServer(registry_server_service_pb2.RegisterServerRequest(server_name=self.name,ip=self.address,port=int(self.port)))
            if response.status == registry_server_service_pb2.Status.SUCCESS:
                print("SUCCESS")
            else:
                print("FAILED")
        return response.status
    
    def __serve(self):

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
