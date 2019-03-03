# coding: utf-8

#to create a socket
import socket
#regex
import re
#system to get the args of the user via the command line
import sys 
#command parser
import argparse 
# to store the headers
import json
#to call the methods and create an object of the other file
from myRequest import * 
import requests


# Display menu options
def display_help():
    print("httpc is a curl-like application but supports HTTP protocol only.\n")
    print("Usage:\n")
    print("\t\thttpc command [arguments]\n")
    print("The commands are:\n")
    print("\t\tget executes a HTTP GET request and prints the response.\n")
    print("\t\tpost executes a HTTP POST request and prints the response.\n")
    print("\t\thelp prints this screen. \n\n")
    print("Use 'httpc help [command]' for more information about a command.")


def display_help_get():
    print("Usage: httpc get [-v] [-h key:value] URL \n\n")
    print("Get executes a HTTP GET request for a given URL.\n")
    print("-v\t\t Prints the detail of the response such as protocol, status, and headers.\n")
    print("-h key:value\t\tAssociates headers to HTTP Request with the format 'key:value'.\n")
    print("-o FileName \t\t Prints the details of the demanded protocol to a file of the given name. \n")


def display_help_post():
    print("Usage: httpc post [-v] [-h key:value] [-d inline-data] [-f file] URL \n\n")
    print("Post executes a HTTP POST request for a given URL with inline data or from file.\n\n")
    print("-v\t\t Prints the detail of the response such as protocol, status, and headers.\n")
    print("-h key:value\t\tAssociates headers to HTTP Request with the format 'key:value'.\n")
    print("-d string\t\tAssociates an inline data to the body HTTP POST request.\n")
    print("-f file\t\tAssociates the content of a file to the body HTTP POST request.\n\n")
    print("Either [-d] or [-f] can be used but not both.\n")


# for the file format, for it to be
# valid it should put the data as
# key value
# key value
# etc
# function returns a python dictionary
def set_file_input(file_name_):
    file = open(file_name_, "r")
    line = file.readline()
    file_data = {}
    while line is not None:
        line_decomp = line.split()
        file_data[line_decomp[0]] = line_decomp[1]
    return file_data


def to_dict(string):

    string_decomp = string.split(':')
    dictionary = {string_decomp[0]:string_decomp[1]}

    return dictionary

# set the port
port = 54321
# set verbose
verbose = 0
isInlineData = 0
isInFile = 0
header = ''
url = ''

# url matching
patternFull = '(?:http.*://)?(?P<host>[^:/ ]+).?(?P<path>[^?]*).*?(?P<query>[^:/]*)'
regex = re.compile(patternFull)

# set user agent
userAgent = 'User-agent: Concordia-HTTP/1.0'


# Print system arguments
arguments = ' '.join(sys.argv[1:])
# loop through the string
if arguments == 'help':
    display_help()
elif arguments == 'help get':
    display_help_get()
elif arguments == 'help post':
    display_help_post()
else:
    # if there is get
    arguments = arguments.split()
    
    if arguments[0] == 'get':
        for index in arguments:
            if index == '-v':
                verbose = 1
            if regex.match(index):
                url = index
        m = re.search(patternFull, url)
        host = m.group('host')
        # method pourrait etre appelé path en vrai
        path = m.group('path')
        prm = m.group('query')
        # to remove the ? after the method (get|post)
        query = prm[1:]
        request = (path+'?'+query)
        # to get the path and query to set to the message to sent
        request = '\r\n'.join(('GET /' + request + ' HTTP/1.0', userAgent, 'Host: ' + host, '', ''))
    
    # if there is post
    if arguments[0] == 'post':
        header = None
        indata = None
        # file_input = None
        file_name = None
        verbose = 0
        # creating the values of which will be used in request
        for index, item in enumerate(arguments):
            if item == '-v':
                verbose = 1

            if regex.match(item):
                url = item

            if item == '-h':
                header = (arguments[index+1])
                header = to_dict(header)

            if item == '-d':
                isInlineData =1
                indata = (arguments[index+1])

            if item == '-f':
                isInFile = 1
                file_name = (arguments[index+1])
                # file_input = set_file_input(file_name)

            if isInFile == 1 and isInlineData ==1:
                print('Only -f or -d can be selected not both. \nby Default -d is selected')
                isInFile = 0
                file_input = None

        m = re.search(patternFull, url)
        host = m.group('host')
        # request = '\r\n'.join(('POST /post HTTP/1.0', userAgent, 'Host: ' + host, 'Content-Type: application/json', 'Content-Length: 17\r\n\r\n'))
        
        # IL FAUT CHANGER CA PR QUE CA ACCEPTE LE INLINE DATA
        # request += '{"Assignmment":1}'
        
        # request = '\r\n'.join(('POST /post HTTP/1.0', userAgent, 'Host: ' + host, header, 'Content-Length: 17\r\n\r\n'))
        # if(isInlineData == 1):
        #    request += indata
        # print request

    # for index in arguments:
    #      if re.search(patternFull, index):
    #         m = index
    #         #to get each component of the URL 
    #         host = m.group('host')
    #         #method pourrait etre appelé path en vrai
    #         path = m.group('path')
    #         prm = m.group('query')
    #         #to remove the ? after the method (get|post)
    #         query = prm[1:]
    #         request = (path+'?'+query)
    #     if index == 'get':
    #         #to get the path and query to set to the message to sent
    #         request = '\r\n'.join(('GET /' + request +  ' HTTP/1.0', userAgent, 'Host: ' + host, '', ''))
    #     if index == 'post':
    #         request = '\r\n'.join(('POST /post HTTP/1.0', userAgent, 'Host: ' + host, 'Content-Type: application/json', 'Content-Length: 17\r\n\r\n'))
    #         request += '{"Assignmment":1}'
    #     if index == '-v':
    #         verbose = 1
    #     if index == '-h':
    #         header = index+1

# HELP MENU DISPLAY

    # if (fct== 'get'):
    #     #regex to get the host name
    #     patternFull = '(?:http.*://)?(?P<host>[^:/ ]+).?(?P<path>[^?]*).*?(?P<query>[^:/]*)'
    #     m = re.search(patternFull, args.pos2)
    #     #to get each component of the URL 
    #     host = m.group('host')
    #     #method pourrait etre appelé path en vrai
    #     path = m.group('path')
    #     prm = m.group('query')
    #     #to remove the ? after the method (get|post)
    #     query = prm[1:]
    #     request = (path+'?'+query)
    #     #to get the path and query to set to the message to sent
    #     request = '\r\n'.join(('GET /' + request +  ' HTTP/1.0', userAgent, 'Host: ' + host, '', ''))
    #     #launch a get request

    # if fct == 'post':
    #     patternFull = '(?:http.*://)?(?P<host>[^:/ ]+).?(?P<path>[^?]*).*?(?P<query>[^:/]*)'
    #     m = re.search(patternFull, args.pos2)
    #     #to get each component of the URL 
    #     patternFull = '(?:http.*://)?(?P<host>[^:/ ]+).?(?P<path>[^?]*).*?(?P<query>[^:/]*)'
    #     m = re.search(patternFull, args.pos2)
    #     #to get each component of the URL 
    #     host = m.group('host')
        
    #     request = '\r\n'.join(('POST /post HTTP/1.0', userAgent, 'Host: ' + host, 'Content-Type: application/json', 'Content-Length: 17\r\n\r\n'))
    #     request += '{"Assignmment":1}'
    #     print request


if arguments[0] == 'post' or arguments[0] == 'get':
    # create socket
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error:
        print('Failed to create socket')
        sys.exit()

    try:
        remote_ip = socket.gethostbyname(host)
    except socket.gaierror:
        print('Hostname could not be resolved. Exiting')
        sys.exit()

    # Connect to remote server
    s.connect((socket.gethostname(), 54321))

    # Send data to remote server
    try:
        if arguments[0] == 'get':
            s.sendall(request.encode())
        # case of post:
        else:
            if header is None and indata is None and file_name is None:
                reply = requests.post(url)
            elif header is not None and indata is None and file_name is None:
                reply = requests.post(url, headers=header)
            elif header is not None and indata is not None and file_name is None:
                reply = requests.post(url, headers=header, data=indata)
            elif header is not None and indata is None and file_name is not None:
                with open(file_name) as payload:
                    reply = requests.post(url, headers=header, data=payload)
            elif header is None and indata is not None and file_name is None:
                reply = requests.post(url, data=indata)
            elif header is None and indata is None and file_name is not None:
                with open(file_name) as payload:
                    reply = requests.post(url, data=payload)

    except socket.error:
        print('Send failed')
        sys.exit()

    # Receive data
    if arguments[0] == 'get':
        reply = s.recv(4096).decode()

    # if there is verbose
    if verbose == 1 :
        reply = reply.split('{', 1)[1]
        reply = '{' + reply
        print(reply)
    if verbose == 0:
        if arguments[0] == 'get':
            print(reply)
        else:
            print(reply.text)


