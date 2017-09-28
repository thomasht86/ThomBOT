class Ticker(object):
    def __init__(self,danger_tick_amount=100,moster_tick_amount=600):
        self.__moster_tick_amount = moster_tick_amount
        self.__danger_tick_amount = danger_tick_amount
        self.ticks_till_monster = moster_tick_amount
        self.knocking_ticks_left = 0
        self.enemy_danger_ticks_left = 0

    def reset(self):
        self.ticks_till_monster = self.__moster_tick_amount
        self.knocking_ticks_left = 0
        self.enemy_danger_ticks_left = 0

    def tick(self):
        self.ticks_till_monster -= 1
        self.knocking_ticks_left = max(0,self.knocking_ticks_left - 1)
        self.enemy_danger_ticks_left = max(0,self.enemy_danger_ticks_left - 1)

    def start_other_is_dangerous_ticker(self):
        self.enemy_danger_ticks_left = self.__danger_tick_amount

    def start_you_are_dangerous_ticker(self):
        self.knocking_ticks_left = self.__danger_tick_amount