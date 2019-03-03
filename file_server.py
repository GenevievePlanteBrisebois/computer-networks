# file created by Genevieve Plante-Brisebois 40003112
# comp445 winter 2019


import os
import server_lib


def get_file_list():
    list_f = []
    for (dirpath, dirnames, filenames) in os.walk('.'):
        list_f.extend(filenames)
    return list_f


def get_foo(sck):
    filename = "foo.txt"
    # verification if the file exists
    if os.path.isfile(filename):
        sck.send("Exists \n")
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
    sck.close()


# method for the post function, so that we replace the content of bar or create bar
def post_bar(content, conn):
    filename = "bar.txt"
    # if there is a file called bar overwrite the content
    if os.path.isfile(filename):
        file = open(filename, "w")
        file.write(content)
    # if there is no file called bar
    else:
        message = 'file not existent, creating file and write to file. \n'
        print(message)
        conn.send(message.encode('utf-8'))
        file = open("bar.txt", "w+")
        file.write(content)


def main():
    sck = server_lib.set_socket()
    sck.listen(5)
    # forever running loop to the server to keep it running
    while True:
        client_con, client_add = sck.accept()
        req = server_lib.response_to_client(client_con, client_add)

        # checking the first char of the requests being made in order to react the proper way
        if req.decode('utf-8')[:7] == "GET/foo":
            msg = "getting list of files \n"
            client_con.send(msg.encode('utf-8'))
            get_foo(client_con)
        elif req.decode('utf-8')[:4] == "GET/":
            list_files = get_file_list()
            print(list_files)
            client_con.send(list_files)
        elif req.decode('utf-8')[:8] == "POST/bar":
            # send the string without the POST/bar (so just the content of the file)
            post_bar(req.decode('utf-8')[9:], client_con)

        elif req.decode('utf-8') == "CLOSE":
            client_con.close()


# operate the main function and bring the server online
main()

