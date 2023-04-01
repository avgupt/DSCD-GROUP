import subprocess
import time
import client
from status_pb2 import Status


# Define constants

REPLICA_PORTS = [8080, 8081, 8082]
REPLICA_ADDRESSES = ["localhost:8080", "localhost:8081", "localhost:8082"]
FILE1_NAME = "file1"
FILE1_CONTENT = "This is file 1 text"

# Start registry server
registry_process = subprocess.Popen(['python', 'registry_server_service.py'])
print("registry service pid",registry_process.pid)
# Wait for registry server to start up
time.sleep(1)

# Start replica servers
replica1 = subprocess.Popen(['python', 'server_service.py', str(REPLICA_PORTS[0])])
print("replica1 pid",replica1.pid)
time.sleep(1)
replica2 = subprocess.Popen(['python', 'server_service.py', str(REPLICA_PORTS[1])])
print("replica2 pid",replica2.pid)
time.sleep(1)
replica3 = subprocess.Popen(['python', 'server_service.py', str(REPLICA_PORTS[2])])
print("replica3 pid",replica3.pid)
time.sleep(1)

# Start clients
client1 = client.Client()
client2 = client.Client()

# Wait for clients to start up
time.sleep(1)

write_response1 = client1.write(FILE1_NAME, FILE1_CONTENT, REPLICA_ADDRESSES[0])
assert write_response1.status.type == Status.STATUS_TYPE.SUCCESS, "write status should be SUCCESS"
file1_uuid = write_response1.uuid

read_response1 = client1.read(file1_uuid,REPLICA_ADDRESSES[0])
assert read_response1.status.type == Status.STATUS_TYPE.SUCCESS, "read replica 1 status should be SUCCESS"
assert read_response1.file_name == FILE1_NAME, "read replica 1 file name not correct"
assert read_response1.content == FILE1_CONTENT, "read replica 1 file content not correct"

read_response2 = client1.read(file1_uuid,REPLICA_ADDRESSES[1])
assert read_response2.status.type == Status.STATUS_TYPE.SUCCESS, "read replica 2 status should be SUCCESS"
assert read_response2.file_name == FILE1_NAME, "read replica 2 file name not correct"
assert read_response2.content == FILE1_CONTENT, "read replica 2 file content not correct"

read_response3 = client1.read(file1_uuid,REPLICA_ADDRESSES[2])
assert read_response3.status.type == Status.STATUS_TYPE.SUCCESS, "read replica 3 status should be SUCCESS"
assert read_response3.file_name == FILE1_NAME, "read replica 3 file name not correct"
assert read_response3.content == FILE1_CONTENT, "read replica 3 file content not correct"

delete_response1 = client2.delete(file1_uuid,REPLICA_ADDRESSES[2])
assert delete_response1.type == Status.STATUS_TYPE.SUCCESS, "delete status should be SUCCESS"

read_response4 = client1.read(file1_uuid,REPLICA_ADDRESSES[0])
assert read_response4.status.type == Status.STATUS_TYPE.FAILURE, "read 4 status should be FAILURE"

read_response5 = client1.read(file1_uuid,REPLICA_ADDRESSES[1])
assert read_response5.status.type == Status.STATUS_TYPE.FAILURE, "read 5 status should be FAILURE"

read_response6 = client1.read(file1_uuid,REPLICA_ADDRESSES[2])
assert read_response6.status.type == Status.STATUS_TYPE.FAILURE, "read 6 status should be FAILURE"

# Stop replica servers
replica1.terminate()
replica2.terminate()
replica3.terminate()

# Stop registry server
registry_process.terminate()
