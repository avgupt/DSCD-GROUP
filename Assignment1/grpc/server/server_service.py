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