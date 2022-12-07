import socket
import os

from clnt_srvr import *


IP = "127.0.0.1"
FILE_LOCATION = "c:\\cyber\\cpypst"

def initiate_client_socket():
    my_socket = None
    try:
        # initiate socket
        my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        #  connect to server
        my_socket.connect((IP, PORT))
    except socket.error as e:
        print("booz!!!", e)
    except Exception as e:
        print("booz!!!", e)

    return my_socket

def send_request_to_server(request, my_socket):
    request = str(len(request)).zfill(MSG_LEN) + request
    my_socket.send(request.encode())

def receive_file(request, my_socket):
    req = request.split()
    f_name = req[1]
    answer_file = FILE_LOCATION + '\\' + f_name[f_name.rfind('\\'):]
    print("answer file location: ", answer_file)
    done = False

    with open(answer_file, "wb") as f:
        while not done:
            raw_size = my_socket.recv(MSG_LEN)
            size = raw_size.decode()
            data = None
            if size.isdigit():
                raw_data = my_socket.recv(int(size))
            if raw_data == EOF:
                done = True
            else:
                f.write(raw_data)

def handle_server_response_response(request, my_socket):
    response = None
    if request.upper().startswith("SEND_FILE"):
        receive_file(request, my_socket)
    raw_size = my_socket.recv(MSG_LEN)
    data_size = raw_size.decode()
    if data_size.isdigit():
        raw_response = my_socket.recv(int(data_size))
        response = raw_response.decode().upper()
    os.system("ComputerInfo.txt")


def valid_request(request):
    req_and_prms = request.split()
    if req_and_prms[0].upper() == "TAKE_SCREENSHOT" and len(req_and_prms) == 1:
        return True
    elif req_and_prms[0].upper() == 'SEND_FILE' and len(req_and_prms) == 2:
        return True
    elif req_and_prms[0].upper() == 'DIR':
        return True
    elif req_and_prms[0].upper() == 'DELETE' and len(req_and_prms) == 2:
        return True
    elif req_and_prms[0].upper() == 'COPY' and len(req_and_prms) == 3:
        return True
    elif req_and_prms[0].upper() == 'EXECUTE' and len(req_and_prms) == 2:
        return True
    elif req_and_prms[0].upper() == 'EXIT' and len(req_and_prms) == 1:
        return True
    elif req_and_prms[0].upper() == 'QUIT' and len(req_and_prms) == 1:
        return True

    return False


def handle_user_input(my_socket):
    done = False
    while not done:
        try:
            request = input('please enter a request')
            if valid_request(request):
                send_request_to_server(request, my_socket)
                handle_server_response_response(request, my_socket)
            else:
                print("illegal request")
            done = request.upper() == 'EXIT' or request.upper() == 'QUIT'
        except socket.error as e:
            print("booz!!!", e)
            done = True
        except Exception as e:
            print("booz!!!", e)
            done = True



def main():
    """
    Clients code which sends to server user's name
    and prints server's response
    """

    try:
        my_socket = initiate_client_socket()

        handle_user_input(my_socket)

        # close socket
        my_socket.close()

    except socket.error as msg:
        print("socket failur: ", msg)
    except Exception as msg:
        print("exception: ", msg)



if __name__ == '__main__':
    main()
