import socket
from subprocess import *
import os
import time
import subprocess

HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)


Popen("alacritty  --command ncspot",shell = True, stdout= PIPE )
time.sleep(3)

(r1, w1) = os.pipe2(0)
(r2, w2) = os.pipe2(0)


nc_process = Popen(["nc -U ~/.cache/ncspot/ncspot.sock"], stdin=r1, stdout=w2, encoding='utf8', shell=True)
outfile = os.fdopen(w1, 'w', buffering=1)


def execute(command):
    print(command, file=outfile)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print(f"Connected by {addr}")
        while True:
            data = conn.recv(1024)
            if(data.decode() != ""):
                print("data: " + data.decode())
                execute(data.decode())
                conn, addr = s.accept()
