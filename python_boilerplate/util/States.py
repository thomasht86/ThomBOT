class States(object):
    def __init__(self,ticker_ref):
        self.ticker = ticker_ref

    def is_status_quo(self):
        return self.ticker.knocking_ticks_left == self.ticker.enemy_danger_ticks_left

    def you_are_dangerous(self):
        return self.ticker.knocking_ticks_left > self.ticker.enemy_danger_ticks_left

    def enemy_is_dangerous(self):
        return self.ticker.knocking_ticks_left < self.ticker.enemy_danger_ticks_left
    
    def is_monster_present(self):
        return self.ticker.ticks_till_monster == 0