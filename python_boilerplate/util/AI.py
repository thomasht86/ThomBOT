from numpy import random as r
class AI(object):
    def __init__(self):
        self.smart = False

    def get_move(self):
        #
        # AI GOES HERE
        #
        if not self.smart:
            return self.__send_random_move()

    def __send_random_move(self):
        return r.randint(0,4)
