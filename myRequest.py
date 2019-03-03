
# This  is used to create an object to represent the request of the user
import json


class myRequest(object):
    # defining constructor
    def __init__(self, host, path, query, request_path, verbose, my_headers, my_file, inline, url):
        self.host = host
        self.path = path
        self.query = query
        self.request_path = request_path
        self.verbose = verbose
        if my_headers is not None:
            key_value = my_headers.split()
            key = key_value[0]
            value = key_value[1]
            headers = [key,value]
            self.my_headers = headers
        else:
            self.my_headers = None
        # if we have a get as path
        if path == 'get':
            self.my_file = None
            self.inline = None
        # if we have a post as path
        if path == 'post':
            if my_file is not None:
                self.my_file = my_file
                self.inline = None
            if inline is not None :
                # self.inline = inline
                self.my_file = None
                key = inline[0]
                value = inline[1]
                inline_val = [key,value]
                self.inline = inline_val
        self.url = url

# getters
    def get_url(self):
        return self.url

    def set_url(self, url):
        self.url = url

    def get_host(self):
        return self.host

    def set_host(self, host):
        self.host = host

    def get_path(self):
        return self.path

    def set_path(self, path):
        self.path = path

    def get_query(self):
        return self.query

    def set_query(self, query):
        self.query = query

    def get_request_path(self):
        return self.request_path

    def set_request_path(self):
        self.request_path = (self.path + '?' + self.query)

    def get_verbose(self):
        return self.verbose

    def set_verbose(self, verbose):
        self.verbose = verbose

    def get_headers(self, index):
        return self.my_headers[index]

    def set_headers(self, my_headers):
        self.my_headers = my_headers

    def get_file(self):
        return self.my_file

    def set_file(self, my_file):
        self.my_file = my_file

    def get_data(self):
        return self.myD

    def set_data(self, myD):
        self.myD = myD

    def get_inline(self, index):
        return self.inline[index]
# verbose option
    def is_v(self):
        if self.verbose is True:
            return True






