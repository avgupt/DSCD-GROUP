import pika
import uuid

import  server_service_pb2 as server_proto
import registry_server_service_pb2 as rs_proto

from Article_pb2 import Article, Date


sample_article_1 = Article(id=1, author="Jane", content="hello world", sports="SPORTS")
sample_article_2 = Article(id=1, author="Jane", content="hello world", fashion="FASHION")


ARTICLE_TYPE = {'S': 'sports', 'F': 'fashion', 'P': 'politics'}


class Client(object):

    def __init__(self):
        self.id = str(uuid.uuid1())

        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost'))

        self.channel = self.connection.channel()

        result = self.channel.queue_declare(queue='', exclusive=True)
        self.callback_queue = result.method.queue

        self.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self.on_response,
            auto_ack=True)

        self.response = None
        self.corr_id = None

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body

    def GetServerList(self)->dict:
        request = rs_proto.GetServerListRequest(client_uuid=self.id).SerializeToString()

        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(
            exchange='',
            routing_key='rs_queue',
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ),
            body=request)
        self.connection.process_data_events(time_limit=None)

        response = rs_proto.GetServerListResponse()
        response.ParseFromString(self.response)
        return response
    
    def JoinServer(self, port):
        queue_name = "server_" + str(port) + "_connection"
        request = server_proto.ConnectionRequest(client_uuid=self.id, is_joining=True).SerializeToString()

        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(
            exchange='',
            routing_key=queue_name,
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ),
            body=request)
        self.connection.process_data_events(time_limit=None)

        if not self.response:
            return "FAILED"

        response = server_proto.ConnectionResponse()
        response.ParseFromString(self.response)
        return response

    def LeaveServer(self, port):
        queue_name = "server_" + str(port) + "_connection"
        request = server_proto.ConnectionRequest(client_uuid=self.id, is_joining=False).SerializeToString()

        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(
            exchange='',
            routing_key=queue_name,
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ),
            body=request)
        self.connection.process_data_events(time_limit=5)

        if not self.response:
            return "FAILED"

        response = server_proto.ConnectionResponse()
        response.ParseFromString(self.response)
        return response
    
    def GetArticles(self, port, date=None, type=None, author=None):
        queue_name = "server_" + str(port) + "_article"
        request = server_proto.GetArticlesRequest(client_uuid=self.id,date=date,type=type,author=author).SerializeToString()

        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(
            exchange='',
            routing_key=queue_name,
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ),
            body=request)
        self.connection.process_data_events(time_limit=5)

        if not self.response:
            return

        response = server_proto.GetArticlesResponse()
        response.ParseFromString(self.response)
        return response
    
    def PublishArticle(self, port, sample_article):
        queue_name = "server_" + str(port) + "_article"
        request = server_proto.PublishArticleRequest(client_uuid=self.id, article=sample_article).SerializeToString()

        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(
            exchange='',
            routing_key=queue_name,
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ),
            body=request)
        self.connection.process_data_events(time_limit=None)

        if not self.response:
            return "FAILED: oops"

        response = server_proto.PublishArticleResponse()
        response.ParseFromString(self.response)
        return response


myClient = Client()
print("Starting Client...\n")
print("Client ID: ", myClient.id)

while(True):
    print("\nGetServerList[1], JoinServer[2], LeaveServer[3], GetArticles[4], PublishArticle[5]")
    
    n = int(input())
    if n == 1:
        server_list = myClient.GetServerList().servers
        for server_name in server_list.keys():
            print(server_name + " - " + server_list[server_name])
    elif n > 5:
        print("INVALID REQUEST")
    else:
        port = input("Enter server port: ")
        if n == 2:
            print(myClient.JoinServer(port))
        elif n == 3:
            print(myClient.LeaveServer(port))
        elif n == 4:
            # Assuming valid input
            date = input("Enter date (dd/mm/yyyy): ")
            article_type = input("Enter type (Sports(S), fashion(F), politics(P): ")
            author = input("Enter author: ")
            
            if date != '':
                date = Date(date=int(date.split("/")[0]), month=int(date.split('/')[1]), year=int(date.split('/')[2]))
            else:
                date = None
            if article_type in ARTICLE_TYPE.keys():
                article_type = ARTICLE_TYPE[article_type]
                
            articles = myClient.GetArticles(port, date, article_type, author)
            if articles:
                articles = articles.article_list
                count = 1
                for article in articles:
                    print(count)
                    print(article.WhichOneof('type'))
                    print(article.author)
                    print(str(article.time.date) + '/' + str(article.time.month) + '/' + str(article.time.month))
                    print(article.content)
                    count += 1
        elif n == 5:
            article = sample_article_1
            print(myClient.PublishArticle(port, article))
            # print(myClient.PublishArticle(port, sample_article_2))

