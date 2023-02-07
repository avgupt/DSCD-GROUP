import grpc

import server_pb2 as server_pb2
import server_pb2_grpc as server_pb2_grpc

from protos.Article.Article_pb2 import Article, Date

sample_date_1 = Date(date=1, month="January", year=2023)
sample_date_2 = Date(date=8, month="January", year=2023)
sample_date_3 = Date(date=16, month="February", year=2023)
sample_date_4 = Date(date=21, month="March", year=2023)

sample_article_1 = Article(id=1, author="Jane", time=sample_date_1, content="hello world")
sample_article_2 = Article(id=2, author="John", time=sample_date_2, content="hello world1")
sample_article_3 = Article(id=3, author="Jolly", time=sample_date_1, content="hello world2")
sample_article_4 = Article(id=4, author="Jan", time=sample_date_4, content="hello world3")

class Client:

    def __init__(self, id):
        self.id = id
        self.start()
    
    def connectToServer(self, server_port):
        # TODO(manvi): connect to mentioned server
        pass

    def start(self):
        # TODO(avishi): Refactor code
        # Reference: www.tutorialspoint.com/grpc/grpc_helloworld_app_with_python.htm
        print(self.id)
        with grpc.insecure_channel('localhost:5005' , options=(('grpc.enable_http_proxy', 0),)) as channel:
            stub = server_pb2_grpc.ClientServerStub(channel)
            response = stub.PublishArticle(server_pb2.PublishArticleRequest(client_id=self.id, article=sample_article_1))
            print(response)
            response = stub.PublishArticle(server_pb2.PublishArticleRequest(client_id=self.id, article=sample_article_2))
            print(response)
            response = stub.GetArticles(server_pb2.GetArticlesRequest(client_id=self.id, date=sample_date_2))
            print(response)
            response = stub.PublishArticle(server_pb2.PublishArticleRequest(client_id=self.id, article=sample_article_3))
            response = stub.GetArticles(server_pb2.GetArticlesRequest(client_id=self.id, date=sample_date_1))
            print(response)
            channel.close()

if __name__ == "__main__":
    myClient1 = Client(11)
    myClient1.start()

    myClient2 = Client(22)
    myClient2.start()
