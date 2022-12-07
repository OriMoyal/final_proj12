import socket
from PIL import ImageGrab
import os
from clnt_srvr import *
import  glob
import shutil
import subprocess
from PCInfo import *

ALL_IFS = '0.0.0.0'
SCREENDHOT_LOCATION = "c:\\cyber\\screenshot.jpg"
CHUNCK_SIZE = 1024

def initiate_server_socket():
        server_socket = None
        try:
               # initiating server socket
            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            # the server binds itself to a certain socket
            server_socket.bind((ALL_IFS, PORT))

            # listening to the socket
            server_socket.listen(1)
        except socket.error as e:
            print("booz!!", e)
        except Exception as e:
            print("booz!!!", e)

        return server_socket

def handle_clients(server_socket):
    done = False
    while not done:
        try:
            # accepting a connect request
            client_socket, address = server_socket.accept()
            done = handle_single_client(client_socket)
            client_socket.close()
        except socket.error as e:
            print("booz!!!", e)
            done = True
            client_socket.close()
        except Exception as e:
            print("booz!!!", e)
            done = True
            client_socket.close()


def receive_client_request(client_socket):
    raw_size = client_socket.recv(MSG_LEN)
    size = raw_size.decode()

    if size.isdigit():
        raw_request = client_socket.recv(int(size))
       # split to request and parameters
        request = raw_request.decode()
        req_and_prms = request.split()
        if len(req_and_prms) > 1:
            return req_and_prms[0].upper(), req_and_prms[1:]
        else:
            return req_and_prms[0].upper(), None
    else:
        return None, None

def take_screenshot():
    im = ImageGrab.grab()
    im.save(SCREENDHOT_LOCATION)
    return "screenshot taken"


def send_file(f_name, client_socket):
    done = False
    with open(f_name, "rb") as f:
        while not done:
            data = f.read(CHUNCK_SIZE)
            if data == b'':
                done = True
                data = EOF
            client_socket.send(str(len(data)).zfill(MSG_LEN).encode() + data)

    return "File sent"


def list_folder(fldr):
    # files_list = glob.glob(fldr + '\\*.*')
    # return str(files_list)
    return "ComputerIP.txt"


def delete_file(f_name):
    os.remove(f_name)
    return "fule removed"


def copy_file(f_name, dir_name):
    dest_fle = dir_name + '\\' + f_name[f_name.rfind('\\'):]
    shutil.copy(f_name, dest_fle)
    return "file copied"

def execute(proc):
    try:
        subprocess.call(proc)
    except subprocess.CalledProcessError as e:
        return "boooz " + str(e)
    return "proc executed"

def valid_file(f_name):
    return os.path.isfile(f_name)


def valid_folder(fold_name):
    return os.path.isdir(fold_name)


def  check_client_request(request, params):
    if request.upper() == "TAKE_SCREENSHOT" and params is None:
        return True
    if request.upper() == "EXIT" and params is None:
        return True
    if request.upper() == "QUIT" and params is None:
        return True
    elif request.upper() == "SEND_FILE" and len(params) == 1:
        return valid_file(params[0])
    elif request.upper() == "DIR" and len(params) == 1:
        return valid_folder(params[0])
    elif request.upper() == "DELETE" and len(params) == 1:
        return valid_file(params[0])
    elif request.upper() == "COPY" and len(params) == 2:
        return valid_file(params[0]) and valid_folder(params[1])
    elif request.upper() == "EXECUTE" and len(params) == 1:
        return True
    else:
        return False


def handle_client_request(request, params, client_socket):
    if request == "TAKE_SCREENSHOT":
        return take_screenshot()
    elif request == "SEND_FILE":
        return send_file(params[0], client_socket)
    elif request == "DIR":
        return list_folder(params[0])
    elif request == "DELETE":
        return delete_file(params[0])
    elif request == "COPY":
        return copy_file(params[0], params[1])
    elif request == "EXECUTE":
        return execute(params[0])
    elif request == "QUIT":
        return "disconnecting client"
    elif request == "EXIT":
        return "exiting"
    else:
        return "illegal request"


def send_response_to_client(response, client_socket):
    response = str(len(response)).zfill(MSG_LEN) + response
    resp = response.encode()
    client_socket.send(resp)


def handle_single_client(client_socket):
    done = False
    while not done:
        try:
            request, params = receive_client_request(client_socket)
            valid = check_client_request(request, params)
            if valid:
                response = handle_client_request(request, params, client_socket)
                send_response_to_client(response, client_socket)
            else:
                if request == 'SEND_FILE':
                    send_response_to_client(EOF.decode(), client_socket)
                send_response_to_client("illgal command", client_socket)

            done = request == 'EXIT' or request == 'QUIT'
        except socket.error as e:
            print("booz!! ", e)
            done = True
        except Exception as e:
            print("booozzz!!!", e)
            done = True

    return request == 'EXIT'

def main():
    """
    server main - receives a message returns it to client
    """
    try:
        server_socket = initiate_server_socket()

        handle_clients(server_socket)


        server_socket.close()
    except socket.error as msg:
        print("socket failur: ", msg)
    except Exception as msg:
        print("exception: ", msg)

if __name__ == '__main__':
    main()
