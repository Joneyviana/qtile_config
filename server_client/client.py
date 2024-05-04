import socket
import sys

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 65432  # The port used by the server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    command = ' '.join(sys.argv[1:])
    print(command)
    s.send(command.encode())
    s.close()
