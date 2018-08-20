# !/usr/bin/env python

import random
import socket, select
from time import gmtime, strftime

image = 'server.png'

HOST = '192.168.0.141'
PORT = 34802

connected_clients_sockets = []

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((HOST, PORT))
server_socket.listen(10)

connected_clients_sockets.append(server_socket)


def recvall(sock, msgLen):
    msg = ""
    bytesRcvd = 0

    while bytesRcvd < msgLen:

        chunk = sock.recv(msgLen - bytesRcvd)

        if chunk == "": break

        bytesRcvd += len(chunk)
        msg += chunk

        if "\r\n" in msg: break
    return msg


while True:

    read_sockets, write_sockets, error_sockets = select.select(connected_clients_sockets, [], [])

    for sock in read_sockets:

        if sock == server_socket:

            sockfd, client_address = server_socket.accept()
            connected_clients_sockets.append(sockfd)

        else:
            try:
                data = recvall(sock, 4096)

                if data:

                    txt = data.strip()
                    print '--%s--' % txt

                    if txt == 'GET':
                        sock.sendall('OK\r\n')

                    elif txt == 'GET_SIZE':

                        with open('server.png', 'rb') as f1:
                            file_size = len(f1.read())
                            f1.seek(0)

                        print '--%s--' % file_size

                        file_size = '%s' % file_size
                        sock.sendall('SIZE %s\r\n' % file_size)

                    elif txt == 'GET_IMG':
                        with open(image, 'rb') as fp:
                            image_data = fp.read()

                        msg = '%sEOIMG\r\n' % image_data
                        sock.sendall(msg)

                    elif txt == 'DONE':
                        sock.close()
                        connected_clients_sockets.remove(sock)

            except:
                sock.close()
                connected_clients_sockets.remove(sock)
                continue
server_socket.close()