from util.Ticker import Ticker
from util.States import States
from util.Map import Map
from util.Message import Message
from util.Message import Player
from get_move import _get_move
import random

class AI(object):
    def __init__(self):
        self.ticker = Ticker()
        self.states = States(self.ticker)
        self.message = Message()
        self.map = Map()
        self.you = Player()
        self.enemy = Player()

    def setup(self,info):
        self.message.parse_message(info)
        self.map = self.message.map
        self.map.load_json_map()
        self.you = self.message.you

    def reset_for_next_round(self):
        self.you = Player()
        self.enemy = Player()
        self.map.reset_map()
        self.ticker.reset()

    def update(self, info):
        self.ticker.tick()
        self.message.parse_message(info)
        self.you = self.message.you
        self.possible_moves = self.map.get_neighbours_of(self.you.pos)
        self.enemy = self.message.enemy
        self.__update_danger()
        self.map.update_content(self.message,[self.you.pos,self.enemy.pos])

    def __update_danger(self):
        if self.you.pos in self.map.super_pellets_positions:
            self.ticker.start_you_are_dangerous_ticker()
        if self.enemy.pos in self.map.super_pellets_positions:
            self.ticker.start_other_is_dangerous_ticker()

    def move(self):
        return _get_move(self,self.map)