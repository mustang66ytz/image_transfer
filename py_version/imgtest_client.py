#!/usr/bin/env python

import socket
import sys

HOST = '192.168.0.141'
PORT = 34802

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = (HOST, PORT)
sock.connect(server_address)
fname = 'fromserver.png'

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


try:

    sock.sendall("GET\r\n")
    data = recvall(sock, 4096)

    if data:
        txt = data.strip()
        print '--%s--' % txt

        if txt == 'OK':

            sock.sendall("GET_SIZE\r\n")
            data = recvall(sock, 4096)

            if data:
                txt = data.strip()
                print '--%s--' % txt

                if txt.startswith('SIZE'):

                    tmp = txt.split()
                    size = int(tmp[1])

                    print '--%s--' % size

                    sock.sendall("GET_IMG\r\n")

                    myfile = open(fname, 'wb')

                    amount_received = 0
                    while amount_received < size:
                        data = recvall(sock, 4096)
                        if not data:
                            break
                        amount_received += len(data)
                        print amount_received

                        txt = data.strip('\r\n')

                        if 'EOIMG' in str(txt):
                            print 'Image received successfully'
                            myfile.write(data)
                            myfile.close()
                            sock.sendall("DONE\r\n")
                        else:
                            myfile.write(data)
finally:
    sock.close()