from numpy import random as r
from util.Map import MapIcons as MI
class AI(object):
    def __init__(self,map=None, player=None):
        self.smart = False
        self.map = map
        self.player = player
        self.map_icons = MI()
        self.visited_pos = MoveHistory(length=12, history=[[self.player['y'], self.player['x']]])
        self.moves_made = 0
        self.moves_made_switch_point = 20

    def get_move(self, msg):
        self.player = msg.you
        self.others = msg.others
        if self.moves_made == self.moves_made_switch_point: self.visited_pos.limit = 2
        avail_pellet_moves = []
        avail_new_moves = []
        avail_old_moves = []
        pos = self.player['y'], self.player['x']
        neighbs = self.__get_neighbs_pos(pos)
        for i, n in enumerate(neighbs):
            if self.__super_pellet(n): return i
            elif self.__pellet(n): avail_pellet_moves.append(i)
            elif self.__not_wall(n):
                if self.visited_pos.contains(n): avail_old_moves.append(i)
                else: avail_new_moves.append(i)
        if len(avail_pellet_moves) > 0: move = r.choice(avail_pellet_moves)
        else: move = r.choice(avail_new_moves) if len(avail_new_moves) > 0 else r.choice(avail_old_moves)
        self.visited_pos.news(pos)
        self.moves_made += 1
        return move

    def __super_pellet(self, pos):
        return self.map.content[pos[0]][pos[1]] is self.map_icons.super_pellet

    def __pellet(self, pos):
        return self.map.content[pos[0]][pos[1]] is self.map_icons.pellet

    def __not_wall(self, pos):
        return self.map.content[pos[0]][pos[1]] is not self.map_icons.wall

    def __get_neighbs_pos(self,pos):
        y, x = pos[0], pos[1]
        up = y - 1, x
        right = y, x + 1
        if x + 1 == self.map.width: right = y, 0
        down = y + 1, x
        if y + 1 == self.map.height: down = 0, x
        left = y, x - 1
        neihbs = [up,right,down,left]
        return neihbs
        
class MoveHistory(object):
    def __init__(self,length=1, history=[]):
        self.__history = history
        self.limit = length

    def news(self, pos):
        if not self.contains(pos):
            self.__history.append(pos)
        if len(self.__history) > self.limit:
            del_point = (len(self.__history)) - self.limit
            self.__history = self.__history[del_point:]

    def contains(self, pos):
        for histpos in self.__history:
            if pos[0] == histpos[0] and pos[1] == histpos[1]: return True
        return False

    def __str__(self):
        return str(self.__history)
        
