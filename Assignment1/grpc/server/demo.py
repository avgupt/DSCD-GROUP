from __future__ import print_function

import grpc
import uuid

from protos.Article.Article_pb2 import Article, Date
import server_service_pb2 as server_pb2
import server_service_pb2_grpc as server_pb2_grpc


import logging
import registry_server_service_pb2 as registry_server_service_pb2
import registry_server_service_pb2_grpc as registry_server_service_pb2_grpc
from client_client import Client 


sample_date_1 = Date(date=1, month=1, year=2023)
sample_date_2 = Date(date=8, month=1, year=2023)
sample_date_3 = Date(date=16, month=2, year=2023)
sample_date_4 = Date(date=21, month=3, year=2023)

sample_article_1 = Article(id=1, author="Jane", time=sample_date_1, content="hello world")
sample_article_2 = Article(id=2, author="John", time=sample_date_2, content="hello world1")
sample_article_3 = Article(id=3, author="Jolly", time=sample_date_1, content="hello world2")
sample_article_4 = Article(id=4, author="Jan", time=sample_date_4, content="hello world3")


if __name__ == "__main__":
    myClient1 = Client()
    # name input - path
    # myClient1.connectToServer('localhost:8080')
    sample_date_1 = Date(date=1, month=1, year=2023)
    sample_article_1 = Article(id=1, author="Jane", content="hello world")
    server_name='server_8080'
    server_name2='server_8081'

    myClient1.connectToServer(server_name)
    myClient1.connectToServer(server_name2)

    myClient1.publishArticle(sample_article_1,server_name)
    myClient1.getArticles(server_name=server_name,date=sample_date_1)

    myClient1.leaveServer(server_name)
