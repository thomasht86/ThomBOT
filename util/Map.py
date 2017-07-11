from numpy.linalg import norm

class Map(object):
    def __init__(self,height=31,width=28,pellets_left=240,content=[[]]):
        self.height = height
        self.width = width
        self.pellets_left = pellets_left
        self.content = self.read_json_map(content)
        
    def load_json_map(self, json_map):
        m = json_map['content']
        self.content = [list(json_map[i]) for i in range(self.height)]
        self.height = json_map['height']
        self.width = json_map['width']
        self.pellets_left = json_map['pelletsleft']

    def dist(self, pos1, pos2, metric='euclid'):
        return pos1.dist(pos2,metric=metric)

class Position(object):
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
        self.coord = [x,y]

    def dist(self, other_pos, metric='euclid'):
        if metric == 'euclid': return norm(other_pos - self.coord)
        else: return abs(other_pos.x - self.x) + abs(other_pos.y - self.y)