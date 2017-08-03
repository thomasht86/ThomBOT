from util.Map import Map
from util.Message import Message as M
from util.Ticker import Ticker as T
from util.Client import Client as C
from util.AI import AI
from timeit import default_timer as timer

def run_bot():
    start = timer()
    while msg.is_stateupdate() or msg.is_welcome():
        map.load_json_map(msg.map)
        move = ai.get_move(msg)
        time = timer() - start
        time *= 1000
        time = round(time,2)
        print("t: %s ms" % str(time))
        c.send_move(move)
        next_gamestate = c.fetch_data()
        start = timer()
        t.tick()
        msg.parse_message(next_gamestate)
    

if __name__ == '__main__':
    c = C()
    json_msg = c.fetch_data()
    msg = M(json_msg)
    map = Map(json_map=msg.map)
    t = T()
    while True:
        msg.await_first_stateupdate_message(c)
        ai = AI(map, msg.you)
        run_bot()
    
