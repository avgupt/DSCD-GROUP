import pika
import uuid

from datetime import date
import datetime

from google.protobuf.message import DecodeError

from Article_pb2 import Article, Date
import  server_service_pb2 as server_proto
import registry_server_service_pb2 as rs_proto


max_clients = 10

class Server:

    def __init__(self, port, name):
        self.address = "localhost"
        self.port = port                        # str - Assuming unique port
        self.hosted_articles = []               # Article[]
        self.subscribers = []                   # Client[]
        self.clientele = []                     # Client[]

        self.name = name

        # Establish connection
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost'))
        self.channel = self.connection.channel()

        # Declare queues
        self.response_queue = self.channel.queue_declare(queue='')
        self.article_queue = self.channel.queue_declare(queue="server_" + self.port + "_article")
        self.connection_queue = self.channel.queue_declare(queue="server_" + self.port + "_connection")

    
    def __getRegistryServerRequest(self):
        return rs_proto.RegisterServerRequest(server_name=self.name,ip=self.address,port=int(self.port))

    def start(self):
        if not self.__isRegistered():
            print("FAIL\n")
        else:
            print("SUCCESS\n")
            self.__serve()

    def __isRegistered(self)->bool:
        # TODO(avishi): implementation
        request = self.__getRegistryServerRequest().SerializeToString()

        self.callback_queue = self.response_queue.method.queue

        # Breaks when correlation id is matched
        self.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self.on_response,
            auto_ack=True)

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
        

        response = rs_proto.RegisterServerResponse()
        response.ParseFromString(self.response)

        if response.status == rs_proto.Status.SUCCESS:
            return True
        return False

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body
    
    def __serve(self):
        self.channel.basic_qos(prefetch_count=1)

        self.channel.basic_consume(queue="server_" + self.port + "_connection", on_message_callback=self.__handleConnectionRequest)
        self.channel.basic_consume(queue="server_" + self.port + "_article", on_message_callback=self.__handleArticleRequest)

        self.channel.start_consuming()


    def __handleConnectionRequest(self, ch, method, props, body):
        try: 
            request = server_proto.ConnectionRequest()
            request.ParseFromString(body)

            if request.is_joining:
                ch.basic_publish(exchange='',
                    routing_key=props.reply_to,
                    properties=pika.BasicProperties(correlation_id = \
                                                        props.correlation_id),
                    body=self.__joinServer(request))

            else:
                ch.basic_publish(exchange='',
                                routing_key=props.reply_to,
                                properties=pika.BasicProperties(correlation_id = \
                                                                    props.correlation_id),
                                body=self.__leaveServer(request))

        except DecodeError:
            ch.basic_publish(exchange='',
                routing_key=props.reply_to,
                properties=pika.BasicProperties(correlation_id = \
                                                    props.correlation_id),
                body=server_proto.ConnectionResponse(status=server_proto.ConnectionResponse.Status.FAILED).SerializeToString())
    
        ch.basic_ack(delivery_tag=method.delivery_tag)  

    def __handleArticleRequest(self, ch, method, props, body):
        request = server_proto.GetArticlesRequest()
        request.ParseFromString(body)

        if request.is_get:
            request = server_proto.GetArticlesRequest()
            request.ParseFromString(body)
            print(request)
            ch.basic_publish(exchange='',
                routing_key=props.reply_to,
                properties=pika.BasicProperties(correlation_id = \
                                                    props.correlation_id),
                body=self.__getArticles(request))


        else:
            request = server_proto.PublishArticleRequest()
            request.ParseFromString(body)
            ch.basic_publish(exchange='',
                            routing_key=props.reply_to,
                            properties=pika.BasicProperties(correlation_id = \
                                                                props.correlation_id),
                            body=self.__publishArticle(request))

        ch.basic_ack(delivery_tag=method.delivery_tag)  


    def __joinServer(self, request):
        # Assuming unique UUID for client.
        client_uuid = request.client_uuid
        print('JOIN REQUEST FROM', client_uuid)
        
        if len(self.clientele) < max_clients:
            self.clientele.append(client_uuid)
            # Success: client accepted and added to clientale.
            return server_proto.ConnectionResponse(status=server_proto.ConnectionResponse.Status.SUCCESS).SerializeToString()
        
        # Failure: Client not added to the clientale list
        return server_proto.ConnectionResponse(status=server_proto.ConnectionResponse.Status.FAILED).SerializeToString()

    def __leaveServer(self, request):
        # Assuming unique UUID for client
        client_uuid = request.client_uuid
        print("LEAVE REQUEST FROM", client_uuid)
        
        if (client_uuid in self.clientele):
            self.clientele.remove(client_uuid)
            return server_proto.ConnectionResponse(status=server_proto.ConnectionResponse.Status.SUCCESS).SerializeToString()

        return server_proto.ConnectionResponse(status=server_proto.ConnectionResponse.Status.FAILED).SerializeToString()


    def __compareTime(self,article_time, request_articles_time):
        article_date_object = datetime.datetime(article_time.year, article_time.month, article_time.date) # date in yyyy/mm/dd format
        request_articles_date_object = datetime.datetime(request_articles_time.year, request_articles_time.month, request_articles_time.date)
        return article_date_object >= request_articles_date_object

    def __filterArticles1(self, time):
        filtered = []
        for article in self.hosted_articles:
            if self.__compareTime(article.time, time):
                filtered.append(article)
        return filtered
    
    def __filterArticles2(self, time, author):
        filtered = []
        for article in self.hosted_articles:
            if self.__compareTime(article.time, time) and article.author == author:
                filtered.append(article)
        return filtered

    def __filterArticles3(self, time, author, article_type):
        filtered = []
        for article in self.hosted_articles:
            if self.__compareTime(article.time, time) and article.author == author and article.WhichOneof('type') == article_type:
                filtered.append(article)
        return filtered
     

    def __getArticles(self, request):
        # Assuming a valid request
        print('ARTICLES REQUEST FROM', request.client_uuid)
        filtered = []
        if request.client_uuid not in self.clientele:
            return server_proto.ConnectionResponse(status=server_proto.ConnectionResponse.Status.FAILED).SerializeToString()

        date = request.date
        if request.date and (request.date.year == 0 or request.date.month == 0 or request.date.date == 0):
            date = None
        if date and request.author and request.type:
            filtered = self.__filterArticles3(date, request.author, request.type)
        elif date and request.author:
            filtered = self.__filterArticles2(date, request.author)
        elif date:
            filtered = self.__filterArticles1(date)
        else:
            filtered = self.hosted_articles

        return server_proto.GetArticlesResponse(article_list=filtered).SerializeToString()
    
    def __publishArticle(self, request):
        print('ARTICLES PUBLISH FROM', request.client_uuid)

        if request.client_uuid not in self.clientele:
            # print("OHNO")
            return server_proto.PublishArticleResponse(status=server_proto.PublishArticleResponse.Status.FAILED).SerializeToString()
        
        today_date = date.today()
        date_object = Date(date=int(today_date.day), month=int(today_date.month),year=int(today_date.year))
        if (request.article.WhichOneof('type') == "sports"):
            article =  Article(id=request.article.id, author=request.article.author, time=date_object, content=request.article.content, sports="SPORTS")
        elif (request.article.WhichOneof('type') == "fashion"):
            article =  Article(id=request.article.id, author=request.article.author, time=date_object, content=request.article.content, fashion="FASHION")
        else:
            article =  Article(id=request.article.id, author=request.article.author, time=date_object, content=request.article.content, politics="POLITICS")

        self.hosted_articles.append(article)
        return server_proto.PublishArticleResponse(status=server_proto.PublishArticleResponse.Status.SUCCESS).SerializeToString()



name = input("Enter name: ")
port = input("Enter port: ") # Assuming valid input
max_clients = int(input("Enter MAXCLIENTS: "))  # Assuming valid input

print("Starting Server...\n")
Server(port, name).start()
