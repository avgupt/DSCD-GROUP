import pika
import uuid

import  server_service_pb2 as server_proto
import registry_server_service_pb2 as rs_proto

from Article_pb2 import Article, Date

sample_date_1 = Date(date=1, month=1, year=2023)


sample_article_1 = Article(id=1, author="Jane", time=sample_date_1, content="hello world")


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
        self.connection.process_data_events(time_limit=None)

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
        self.connection.process_data_events(time_limit=None)

        response = server_proto.ConnectionResponse()
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

        response = server_proto.ConnectionResponse()
        response.ParseFromString(self.response)
        return response


myClient = Client()

while(True):
    print("GetServerList[1], JoinServer[2], LeaveServer[3], GetArticles[4], PublishArticle[5]:")
    n = int(input())

    if n == 1:
        print(myClient.GetServerList())

    else:
        port = input("Enter server port: ")

        if n == 2:
            print(myClient.JoinServer(port))
        
        elif n == 3:
            print(myClient.LeaveServer(port))
        
        elif n == 4:
            # TODO: take input
            print(myClient.GetArticles(port))
        
        else:
            article = sample_article_1
            print(myClient.PublishArticle(port, article))
