from util.Ticker import Ticker
from util.States import States
from util.Map import Map
from util.Message import Message
from util.Message import Player
import numpy as np

class AI(object):
    def __init__(self):
        self.values = Values()
        self.ticker = Ticker()
        self.states = States(self.ticker)
        self.message = Message()
        self.map = Map()
        self.map.register_cost_and_heuristic(self.astar_move_cost,self.astar_heuristic)
        self.you = Player()
        self.enemy = Player()

    def setup(self,info):
        self.message.parse_message(info)
        self.map = self.message.map
        self.map.load_json_map()
        self.player = self.message.you

    def reset_for_next_round(self):
        self.you = Player()
        self.enemy = Player()
        self.map.reset_map()
        self.ticker.reset()


    def update(self, info):
        self.ticker.tick()
        self.message.parse_message(info)
        self.player = self.message.you
        self.possible_moves = self.map.get_neighbours_of(self.player.pos)
        self.enemy = self.message.enemy
        self.__update_danger()
        new_poses = [self.player.pos,self.enemy.pos]
        self.map.update_content(self.message,new_poses)

    def __update_danger(self):
        if self.player.pos in self.map.super_pellets_positions:
            self.ticker.start_you_are_dangerous_ticker()
        if self.enemy.pos in self.map.super_pellets_positions:
            self.ticker.start_other_is_dangerous_ticker()

    def get_move(self): # AI LOGIC GOES HERE!
        if self.states.is_status_quo():
            path = self.map.get_bf_path(self.player.pos,char_goal=self.map.icon.pellet)
            first_move_pos = path[1]
            move = self.map.get_move_from(self.player.pos,first_move_pos)
            return move
        elif self.states.you_are_dangerous():
            path = self.map.get_bf_path(self.player.pos,pos_goal=self.enemy.pos)
            first_move_pos = path[1]
            move = self.map.get_move_from(self.player.pos,first_move_pos)
            return move
        elif self.states.enemy_is_dangerous():
            if self.map.get_euclidean_dist(self.you.pos,self.enemy.pos) <= self.values.enemy_distance_trigger:
                return self.send_random_move()
            else:
                path = self.map.get_bf_path(self.player.pos,char_goal=self.map.icon.pellet)
                first_move_pos = path[1]
                return self.map.get_move_from(self.player.pos,first_move_pos)

        return -1 #haha, you messed up!  :P
    
    def send_random_move(self):
        return self.map.get_move_from(self.player.pos,np.random.choice(list(self.possible_moves)))

    def astar_heuristic(self,start,goal):
        return self.map.get_euclidean_dist(start,goal)

    def astar_move_cost(self,pos1,pos2):
        return 10.0

class Values(object):
    def __init__(self,pellet_worth=1.0,super_pellet_worth=5.0,enemy_distance_trigger=100.0,monster_distance_trigger=9.0):
        self.pellet_worth = pellet_worth
        self.super_pellet_worth = super_pellet_worth
        self.enemy_distance_trigger = enemy_distance_trigger
        self.monster_distance_trigger = monster_distance_trigger