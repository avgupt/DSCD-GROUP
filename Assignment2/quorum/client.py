from datetime import datetime

import grpc, uuid
import protos.registry_server_service_pb2_grpc as registry_server_service_pb2_grpc
import protos.server_service_pb2_grpc as server_service_pb2_grpc

from protos.registry_server_service_pb2 import Request
from protos.server_service_pb2 import WriteRequest, FileRequest
from protos.status_pb2 import Status

REQUEST_PRINT_MSG = "Sending request to"
RESPONSE_PRINT_MSG = "Response received"

def get_servers(request_type):
    with grpc.insecure_channel('localhost:8888') as channel:
        stub = registry_server_service_pb2_grpc.RegistryServerServiceStub(channel)
        return stub.getServers(Request(type=request_type)).server_list

def print_all_servers():
    for server in get_servers(Request.REQUEST_TYPE.GET):
        print(server.port)

def get_version(timestamp):
    date_ = timestamp.date
    date_str = str(date_.day) + "/" + str(date_.month) + "/" + str(date_.year)
    time_ = timestamp.time
    time_str = str(time_.hour) + ":" + str(time_.minute) + ":" + str(time_.second)
    return date_str + " " + time_str

def get_status_bool(status):
    if status.type == Status.STATUS_TYPE.FAILURE:
        print("Status: FAILURE")
        print("Message:", status.message)
        return False
    else:
        print("Status: SUCCESS")
        return True

def print_write_response(response):
    if get_status_bool(response.status):
        print("UUID", response.uuid)
        print("Version:", get_version(response.version))


def write(name, content, uuid):
    server_list = get_servers(Request.REQUEST_TYPE.WRITE)
    for server in server_list:
        server_address = server.ip + ":" + server.port
        print(REQUEST_PRINT_MSG, server_address)
        with grpc.insecure_channel(server_address) as channel:
            stub = server_service_pb2_grpc.ServerServiceStub(channel)
            response = stub.write(WriteRequest(file_name=name, file_content=content, uuid=uuid))
            print(RESPONSE_PRINT_MSG)
        print_write_response(response)

def get_datetime_obj(timestamp):
    return datetime(
        day=timestamp.date.day, month=timestamp.date.month, year=timestamp.date.year,
        hour=timestamp.time.hour, minute=timestamp.time.minute, second=timestamp.time.second
    )

def compare_timestamp(t1, t2):
    ''' Returns if t1 > t2 '''
    if not t2:
        # Assumption: t1 can never be None
        return True
    return get_datetime_obj(t1) > get_datetime_obj(t2)

def print_read_response(response, server):
    print("Printing response from", server)
    if get_status_bool(response.status):
        print("Name:", response.file_name)
        print("Content:", response.content)
        print("Version", get_version(response.version))


def read(uuid):
    server_list = get_servers(Request.REQUEST_TYPE.READ)
    latest_timestamp = None
    latest_response = None
    latest_server = None
    for server in server_list:
        server_address = server.ip + ":" + server.port
        print(REQUEST_PRINT_MSG, server_address)
        with grpc.insecure_channel(server_address) as channel:
            stub = server_service_pb2_grpc.ServerServiceStub(channel)
            response = stub.read(FileRequest(uuid=uuid))
            print(RESPONSE_PRINT_MSG)
        if response.status.type == Status.STATUS_TYPE.FAILURE:
            latest_response = response
            latest_server = server_address
            print_read_response(latest_response, latest_server)
            return None
        elif compare_timestamp(response.version, latest_timestamp):
            latest_timestamp = response.version
            latest_response = response
            latest_server = server_address
    print_read_response(latest_response, latest_server)        


def delete(uuid):
    server_list = get_servers(Request.REQUEST_TYPE.DELETE)
    for server in server_list:
        server_address = server.ip + ":" + server.port
        print(REQUEST_PRINT_MSG, server_address)
        with grpc.insecure_channel(server_address) as channel:
            stub = server_service_pb2_grpc.ServerServiceStub(channel)
            response = stub.delete(FileRequest(uuid=uuid))
            print(RESPONSE_PRINT_MSG)
        get_status_bool(response)   

# MAIN
uuid_string_1 = str(uuid.uuid1())
uuid_string_2 = str("hghd87377673")
print(uuid_string_1, uuid_string_2)

print_all_servers()
x = input("Intervention: ")
write("hello_world_new", "this is testing", uuid_string_1)
x = input("Intervention: ")
read(uuid_string_1)
x = input("Intervention: ")
read(uuid_string_2)
x = input("Intervention: ")
delete(uuid_string_2)
x = input("Intervention: ")
delete(uuid_string_1)
