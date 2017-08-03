import socket
from numpy import random as r
class Client(object):
    def __init__(self,bot_name=b"NAME Superiority\n"):
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__connect()
        self.__socket.send(bot_name)

    def __connect(self):
        host = '127.0.0.1'
        port = 54321
        self.__socket.connect((host,port))

    def fetch_data(self):
        data = b''
        while b'\n' not in data:
            data += self.__socket.recv(4096)
        return data.split(b'\n')[0]

    def send_move(self, move):
        if (move == 0): self.__send_up()
        elif (move == 1): self.__send_right()
        elif (move == 2): self.__send_down()
        elif (move == 3): self.__send_left()
        else:
            print("didn't send anything") #you done goofed!

    def __send_up(self):
        self.__socket.send(b"up\n")

    def __send_right(self):
        self.__socket.send(b"right\n")

    def __send_down(self):
        self.__socket.send(b"down\n")

    def __send_left(self):
        self.__socket.send(b"left\n")
