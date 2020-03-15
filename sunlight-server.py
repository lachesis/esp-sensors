#!/usr/bin/env python3
import socket

HOST = ''                 # Symbolic name meaning all available interfaces
PORT = 4004

animation = ['0,0,5,5']
ani_iter = iter(animation)

print('Listening', PORT)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
s.bind((HOST, PORT))
s.listen(1)

while True:
    conn, addr = s.accept()
    print('Connected by', addr)
    data = conn.recv(1024).decode()
    for line in data.split('\n'):
        print('>', line)
        if line.startswith('?'):
            try:
                out = next(ani_iter)
            except StopIteration:
                ani_iter = iter(animation)
                out = next(ani_iter)
            print('<', out)
            conn.sendall((out + "\n").encode())
        elif line.startswith('!'):
            animation = [line.strip()[1:]]
            ani_iter = iter(animation)
        elif line.startswith('+'):
            animation.append(line.strip()[1:])
    conn.close()


