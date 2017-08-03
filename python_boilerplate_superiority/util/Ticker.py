class Ticker(object):
    def __init__(self):
        self.game_tick = 0
        self.tick_till_monster = 600
        self.tick_left_of_super = 0

    def tick(self):
        self.game_tick += 1
        self.tick_till_monster -= 1
        if self.tick_left_of_super > 0: self.tick_left_of_super -= 1

    def start_super_countdown(self):
        self.tick_left_of_super = 100