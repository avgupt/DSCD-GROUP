import subprocess
import time
import client


# Define constants

REPLICA_PORTS = [8080, 8081, 8015]



# Start registry server
registry_process = subprocess.Popen(['python', 'registry_server_service.py'])

# Wait for registry server to start up
time.sleep(1)

# Start replica servers
replica1 = subprocess.Popen(['python', 'server_service.py', str(REPLICA_PORTS[0])])
replica2 = subprocess.Popen(['python', 'server_service.py', str(REPLICA_PORTS[1])])


# Wait for replica servers to start up
time.sleep(1)

# Start clients
client1 = client.Client()
client2 = client.Client()

# Wait for clients to start up
time.sleep(1)

write_response1 = client1.write("hello1", "my name is  \n yoyoyo", "localhost:8080")
read_response1 = client1.read(write_response1.uuid,"localhost:8081")

# Stop replica servers
replica1.terminate()
replica2.terminate()

# Stop registry server
registry_process.terminate()
