import subprocess
import time
import client
from status_pb2 import Status
import uuid


# Define constants

REPLICA_PORTS = [8080, 8081, 8082]
REPLICA_ADDRESSES = ["localhost:8080", "localhost:8081", "localhost:8082"]
FILE1_NAME = "file1.txt"
FILE1_CONTENT = "This is file 1 text"

FILE2_NAME = "file2.txt"
FILE2_CONTENT = "This is file 2 text"

# Start registry server
registry_process = subprocess.Popen(['python', 'registry_server_service.py'])
print("registry service pid", registry_process.pid)
# Wait for registry server to start up
time.sleep(5)
print()

# Start replica servers
replica1 = subprocess.Popen(['python', 'server_service.py', str(REPLICA_PORTS[0])])
print("replica1 pid", replica1.pid)
time.sleep(5)
print()

replica2 = subprocess.Popen(['python', 'server_service.py', str(REPLICA_PORTS[1])])
print("replica2 pid", replica2.pid)
time.sleep(5)
print()

replica3 = subprocess.Popen(['python', 'server_service.py', str(REPLICA_PORTS[2])])
print("replica3 pid", replica3.pid)
time.sleep(5)
print()

# Start clients
client1 = client.Client()
# client2 = client.Client()

# Wait for clients to start up
time.sleep(5)

# Task 1 
print("Start: Task 1")
file1_uuid = str(uuid.uuid1())
write_response1 = client1.write(FILE1_NAME, FILE1_CONTENT, file1_uuid, REPLICA_ADDRESSES[0])
file1_uuid = write_response1.uuid
print()

for i in REPLICA_ADDRESSES:
    print("Server", i)
    read_response = client1.read(file1_uuid, i)
    time.sleep(5)
    print()

print("End: Task 1\n")

# Task 2
print("Start: Task 2")
file2_uuid = str(uuid.uuid1())
write_response2 = client1.write(FILE2_NAME, FILE2_CONTENT, file2_uuid, REPLICA_ADDRESSES[1])
file2_uuid = write_response2.uuid
print()

for i in REPLICA_ADDRESSES:
    print("Server", i)
    read_response = client1.read(file2_uuid, i)
    time.sleep(5)
    print()

print("End: Task 2\n")

# Task 3
print("Start: Task 3")
delete_response1 = client1.delete(file2_uuid, REPLICA_ADDRESSES[2])
print()

for i in REPLICA_ADDRESSES:
    print("Server", i)
    read_response = client1.read(file2_uuid, i)
    time.sleep(5)
    print()

print("End: Task 3\n")

# Stop replica servers
replica1.terminate()
replica2.terminate()
replica3.terminate()

# Stop registry server
registry_process.terminate()
