import socket
from AI import AI
from util.Message import get_message_type
from timeit import default_timer as time

class Client(object):
    def __init__(self,bot_name):
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

    def setup_bot(self):
        self.ai = AI()
        self.ai.setup(self.fetch_data())

    def await_round_start_message(self):
        json_msg = self.fetch_data()
        while not (get_message_type(json_msg) == 'startofround'):
            json_msg = self.fetch_data()
        while not (get_message_type(json_msg) == 'stateupdate'):
            json_msg = self.fetch_data()
        return json_msg
    
    def run_bot(self):
        while True:
            msg = self.await_round_start_message()
            while get_message_type(msg) == 'stateupdate':
                start = time()
                self.ai.update(msg)
                move = self.ai.get_move()
                duration = time() - start
                print("ai took: {0}ms".format(round(duration * 1000,2)))
                self.send_move(move)
                msg = self.fetch_data()
            self.ai.reset_for_next_round()

    def send_move(self, move): #clockwise motherfucker!  can you digg it!?
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