from util.Map import Map
from util.Message import Message as M
from util.Ticker import Ticker as T
from util.Client import Client as C
from util.AI import AI

def run_bot():
    while msg.is_stateupdate() or msg.is_welcome():
        map.load_json_map(msg.map)
        move = ai.get_move()
        c.send_move(move)
        next_gamestate = c.fetch_data()
        t.tick()
        msg.parse_message(next_gamestate)

if __name__ == '__main__':
    bot_name = b"NAME [your bot's NAME]\n" # <--- bot name goes here (same as file_NAME)
    c = C(bot_name = bot_name)
    json_msg = c.fetch_data()
    msg = M(json_msg)
    map = Map(json_map=msg.map)
    t = T()
    while True:
        msg.await_first_stateupdate_message(c)
        ai = AI()
        run_bot()
