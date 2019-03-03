# file created by Genevieve Plante-Brisebois 40003112
# comp445 winter 2019


import os
import server_lib


# gets the list of the files in the directory
def get_file_list():
    list_f = []
    for (dirpath, dirnames, filenames) in os.walk('.'):
        list_f.extend(filenames)
    final_msg = ""
    for x in list_f:
        final_msg += x
        final_msg += ", \n"

    return final_msg


# gets the content of the foo file
def get_foo(sck):
    filename = "foo.txt"
    # verification if the file exists
    if os.path.isfile(filename):
        msg = "\nExists \n"
        sck.send(msg.encode('utf-8'))
        # while the file is open we send the content 1024 byte at the time
        with open(filename, 'rb') as file:
            file_to_byte = file.read(1024)
            sck.send(file_to_byte)

            # make sure to stop when the file is done
            while file_to_byte != "":
                file_to_byte = file.read(1024)
                sck.send(file_to_byte)

    # if the file is not in the directory then we send the error message
    else:
        msg = "Error 404 - File does not exist \n"
        sck.send(msg.encode('utf-8'))


# method for the post function, so that we replace the content of bar or create bar
def post_bar(content, conn):
    filename = "bar.txt"
    # if there is a file called bar overwrite the content
    if os.path.isfile(filename):
        file = open(filename, "w")
        file.write(content)
        file.close()
    # if there is no file called bar
    else:
        message = 'file not existent, creating file and write to file. \n'
        print(message)
        conn.send(message.encode('utf-8'))
        file = open("bar.txt", "w+")
        file.write(content)
        file.close()


def main():
    sck = server_lib.set_socket()
    sck.listen(5)
    # forever running loop to the server to keep it running
    while True:
        client_con, client_add = sck.accept()
        req = server_lib.response_to_client(client_con, client_add)
        print("\n Request received, handling request \n")
        # checking the first char of the requests being made in order to react the proper way
        if req.decode('utf-8')[:7] == "GET/foo":
            get_foo(client_con)
        elif req.decode('utf-8')[:4] == "GET/":
            msg = "\n getting list of files \n"
            client_con.send(msg.encode('utf-8'))
            list_files = get_file_list()
            print(list_files)
            # final_list = [item.encode('utf-8') for item in list_files]
            # final_list = json.dumps(list_files)
            client_con.send(list_files.encode('utf-8'))
        elif req.decode('utf-8')[:8] == "POST/bar":
            msg = ""
            # send the string without the POST/bar (so just the content of the file)
            post_bar(req.decode('utf-8')[9:], client_con)
        else:
            err = "\n Request invalid, enter a valid request \n"
            client_con.send(err.encode('utf-8'))
        # closing client connection
        msg = "\n request processed. closing connection \n"
        client_con.send(msg.encode('utf-8'))
        client_con.close()


# operate the main function and bring the server online
main()

