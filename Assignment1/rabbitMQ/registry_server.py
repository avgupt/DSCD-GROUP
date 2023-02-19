import pika
from google.protobuf.any_pb2 import Any

import registry_server_service_pb2 as proto 

class RegistryServer:

    def __init__(self, max_servers) -> None:
        self.max_servers = max_servers
        self.servers = {}

        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost'))

        self.channel = self.connection.channel()

        self.channel.queue_declare(queue='rs_queue')

        self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(queue='rs_queue', on_message_callback=self.requestDispatch)

        self.channel.start_consuming()
    
    def requestDispatch(self, ch, method, props, body):

        request = proto.RegisterServerRequest()
        request.ParseFromString(body)

        if request.ip:
            ch.basic_publish(exchange='',
                            routing_key=props.reply_to,
                            properties=pika.BasicProperties(correlation_id = \
                                                                props.correlation_id),
                            body=self.__register(request))

        else:
            request = proto.GetServerListRequest()
            request.ParseFromString(body)
            ch.basic_publish(exchange='',
                            routing_key=props.reply_to,
                            properties=pika.BasicProperties(correlation_id = \
                                                                props.correlation_id),
                            body=self.__getServerList(request))
    
        ch.basic_ack(delivery_tag=method.delivery_tag)        
      


    def __register(self, request):
        # Assuming server_name would be unique, otherwise it can override servers map
        server_name = request.server_name
        ip = request.ip
        port = request.port

        address = ip + ':'+ str(port)
        print("JOIN REQUEST FROM", address)
        if len(self.servers) < self.max_servers:
            self.servers[server_name] = address
            return proto.RegisterServerResponse(status=proto.Status.SUCCESS).SerializeToString()
        return proto.RegisterServerResponse(status=proto.Status.FAILED).SerializeToString()

    def __getServerList(self, request):
        print("SERVICE LIST REQUEST FROM", request.client_uuid)
        return proto.GetServerListResponse(servers=self.servers).SerializeToString()

print("Starting Registry Server...\n")

max_servers = int(input("Enter MAXSERVERS: "))  # Assuming valid input
RegistryServer(max_servers)
