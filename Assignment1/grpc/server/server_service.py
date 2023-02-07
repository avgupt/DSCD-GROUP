from concurrent import futures
import logging

import grpc
import server_pb2, server_pb2_grpc

hosted_articles = []
subscribers = []
clientele = []

class ClientServerServicer(server_pb2_grpc.ClientServerServicer):

    def filterArticles(self, time):
        filtered = []
        for article in hosted_articles:
            if article.time == time:
                filtered.append(article)
        return filtered
    
    def filterArticles(self, time, author):
        filtered = []
        for article in hosted_articles:
            if article.time == time and article.author == author:
                filtered.append(article)
        return filtered

    def filterArticles(self, time, author, article_type):
        filtered = []
        for article in hosted_articles:
            if article.time == time and article.author == author and article.WhichOneof('config') == article_type:
                filtered.append(article)
        return filtered        

    def GetArticles(self, request, context):
        # Assuming a valid request
 
        if request.client_id not in clientele:
            context.cancel() 

        filtered = []

        if request.date and request.author and request.type:
            filtered = self.filterArticles(request.date, request.author, request.type)
        elif request.date and request.author:
            filtered = self.filterArticles(request.date, request.author)
        else:
            filtered = self.filterArticles(request.date)

        return server_pb2.GetArticlesResponse(article_list=filtered)
    
    def PublishArticle(self, request, context):
        if request.client_id not in clientele:
            context.cancel()
            return server_pb2.PublishArticleResponse(server_pb2.PublishArticleResponse.Status.FAILED)
        
        hosted_articles.append(request.article)
        return server_pb2.PublishArticleResponse(server_pb2.PublishArticleResponse.Status.SUCCESS)

class Server:

    def __init__(self, port):
        self.address = "localhost"
        self.port = port                        # str
        self.hosted_articles = []               # Article[]
        self.subscribers = []                   # Client[]
        self.clientele = []                     # Client[]

        self.name = "server_" + port

    def start(self):
        if not self.__isRegistered():
            print("Could not register server")
        else:
            self.__serve()

    def __isRegistered(self)->bool:
        # TODO(guptashelly): call Register RPC and return response
        return True
    
    def __serve(self):
        # TODO(avishi): Refactor code // Remove plag
        # Reference: https://realpython.com/python-microservices-grpc/

        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        server_pb2_grpc.add_ClientServerServicer_to_server(
            ClientServerServicer(), server
        )
        server.add_insecure_port("[::]:" + self.port)
        server.start()
        server.wait_for_termination()

if __name__ == "__main__":
    port = input("Enter port for server: ")

    myServer = Server(port)
    myServer.start()
