class Map(object):
    def __init__(self,height=31,width=28,pellets_left=240,content=[[]],json_map=None):
        self.height = height
        self.width = width
        self.pellets_left = pellets_left
        self.content = content
        if json_map is not None:
            self.load_json_map(json_map)
        
    def load_json_map(self, json_map):
        m = json_map['content']
        self.height = json_map['height']
        self.width = json_map['width']
        self.content = [[m[y][x] for x in range(self.width)] for y in range(self.height)]
        self.pellets_left = json_map['pelletsleft']

    def print_map_content(self):
        for row in self.content:
            s = ""
            for c in row:
                s += c
            print(s)

class MapIcons(object):
    def __init__(self,floor='_',wall='|',door='-',pellet='.',super_pellet='o'):
        self.floor=floor
        self.wall=wall
        self.door=door
        self.pellet=pellet
        self.super_pellet=super_pellet
