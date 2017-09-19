import socket
from util.AI import AI
from util.Message import get_message_type
from timeit import default_timer as time

class Client(object):
    def __init__(self,bot_name):
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__connect()
        self.__socket.send(bot_name)
        self.ticks = 0
        self.tot_time = 0
        self.rounds_avg = []

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
            self.ticks = 0
            self.tot_time = 0
            msg = self.await_round_start_message()
            while get_message_type(msg) == 'stateupdate':
                start = time()
                self.ai.update(msg)
                move = self.ai.move()
                end = time()
                duration = round((end - start) * 1000,2)
                self.tot_time += duration
                self.send_move(move)
                self.ticks += 1
                msg = self.fetch_data()
            avg = round(self.tot_time / self.ticks,2)
            self.rounds_avg.append(avg)
            print("\navg time: {0}ms\n".format(avg))
            self.ai.reset_for_next_round()
            print("rounds avg: {0}ms\n".format(round(sum(self.rounds_avg) / len(self.rounds_avg),2)))

    def send_move(self, move):
        if (move == 0): self.__send_up()
        elif (move == 1): self.__send_right()
        elif (move == 2): self.__send_down()
        elif (move == 3): self.__send_left()
        else:
            print("That's no move!")

    def __send_up(self):
        self.__socket.send(b"up\n")

    def __send_right(self):
        self.__socket.send(b"right\n")

    def __send_down(self):
        self.__socket.send(b"down\n")

    def __send_left(self):
        self.__socket.send(b"left\n")