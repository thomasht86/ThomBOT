import json
from util.Map import Position as Pos
from util.Map import Map

def get_message_type(json_msg):
    dec = json_msg.decode()
    js = json.loads(dec)
    return js['messagetype']

class Message(object):
    def __init__(self):
        self.type = ''
        self.map = Map()
        self.you = Player()
        self.enemy = Player()

    def parse_message(self, json_message):
        dec = json_message.decode()
        js = json.loads(dec)
        self.type = js['messagetype']
        if self.is_welcome():
            print("welcome")
            self.__base_parse_map(js['map'])
            self.__parse_you(js['you'])
        if self.is_stateupdate():
            self.map.pellets_left = js['gamestate']['map']['pelletsleft']
            self.__parse_you(js['gamestate']['you'])
            self.__parse_other(js['gamestate']['others']) 

    def __base_parse_map(self, json_map):
        content,height,pelletsleft,width = json_map['content'], json_map['height'], json_map['pelletsleft'], json_map['width']
        self.map = Map(height=height,width=width,pellets_left=pelletsleft)
        self.map.content = content

    def __parse_you(self, json_you):
        if self.is_welcome():
            id,x,y = json_you['id'],json_you['x'], json_you['y']
            self.you = Player(id=id,pos=Pos(x,y))
        else:
            x,y,score,is_dangerous = json_you['x'], json_you['y'], json_you['score'], json_you['isdangerous']
            self.you.is_dangerous = is_dangerous
            self.you.pos.set(x,y)
            self.you.score = score

    def __parse_other(self, json_other):
        other = json_other[0]
        id,x,y,score,is_dangerous = other['id'], other['x'], other['y'], other['score'], other['isdangerous']
        self.enemy.id = id
        self.enemy.pos.set(x,y)
        self.enemy.score = score
        self.enemy.is_dangerous = is_dangerous

    def is_dead(self):
        return self.type == 'dead'

    def is_welcome(self):
        return self.type == 'welcome'

    def is_stateupdate(self):
        return self.type == 'stateupdate'


    def is_startofround(self):
        return self.type == 'startofround'

    def is_endofround(self):
        return self.type == 'endofround'

class Player(object):
    def __init__(self,pos=Pos(0,0),id=0,score=0,is_dangerous=False):
        self.id = id
        self.pos = pos
        self.score = score
        self.is_dangerous = is_dangerous