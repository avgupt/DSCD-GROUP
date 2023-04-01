#!/bin/bash

Nr=3
Nw=3
N=4
new_server_port=8000
terminal_sleep=1000

xterm -title "Registry Server" -e "python registry_server.py $Nr $Nw $N; sleep $terminal_sleep" &

for server_num in $(seq 1 $N)
do
    sleep 1
    xterm -title "Server - localhost:$new_server_port" -e "python server.py $new_server_port; sleep $terminal_sleep" &
    new_server_port=$((new_server_port + 1))
done

sleep 1
xterm -title "Client" -e "python client.py; sleep $terminal_sleep" &
