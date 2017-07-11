from util.Map import *
from util.Message import Message
from util.Ticker import Ticker as T
from util.Client import Client as connection

def run_bot():
    map = Map()
    t = T()
    data = c.fetch_data()
    msg.parse_message(data)
    while msg.is_stateupdate():
        map.load_json_map(msg.map)
        move = None
        #
        # [YOUR BOT'S AI]
        #
        c.send_random_move() #remove this
        msg.parse_message(c.fetch_data())
        t.tick()
if __name__ == '__main__':
    bot_name = b"NAME [YOUR BOT NAME]\n" # <--- bot name goes here (same as file NAME)
    c = connection(bot_name = bot_name)
    msg = Message(c.fetch_data())
    #TODO handle welcome message
    if msg.is_welcome(): #This is not right anymore
        run_bot()