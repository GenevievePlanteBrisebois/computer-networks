# file created by Genevieve Plante-Brisebois 40003112
# COMP445 winter 2019

import socket
import sys
# import threading


def response_to_client(client_con, client_add):
    test_response = 'welcome to http server \n'
    client_con.send(str.encode(test_response))
    # waiting and establishing the connection with the client
    print('Connected by :', client_add)
    line = bytearray()
    while 1:
        req = client_con.recv(1024)
        if not req:
            break
            # make a exit symbol to be able to end and proccess the request
        if req.decode('utf-8') == '^':
            break
        line.extend(req)
        print('\n')
        print(line.decode('utf-8'))
        print('\n')

    req = line
    client_con.send(req)
    print(req.decode('utf-8'))

    # close the connection
    # print('Closing connection')
    # client_con.close()
    return req


def set_socket():

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #  setting up the socket to implement the server
    HOST, PORT = '', 54321

    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        server_socket.bind((HOST, PORT))
    except socket.error as message:
        print('Bind failed. ', message)
        sys.exit()

    print('Bind successful')
    # queue up to 5 requests
    print('Host: ', HOST)
    print('Server on port:', PORT)
    return server_socket


def main():
    server_socket = set_socket()
    server_socket.listen(5)

# print the information in order to see if the socket is working properly

    print('Server listening...')
# set up the response for the socket and accept a connection

    while True:
        client_con, client_add = server_socket.accept()
        response_to_client(client_con)
        client_con.close()
        print("Server listening ... \n")

    #server_socket.close()

# main()

