import json
class Message(object):
    def __init__(self,json_msg=None):
        if json_msg is None:
            self.type = ''
            self.map = None
            self.you = None
            self.others = []
        else:
            self.parse_message(json_msg)

    def parse_message(self, json_message):
        dec = json_message.decode()
        js = json.loads(dec)
        self.type = js['messagetype']
        if self.is_welcome():
            self.map = js['map']
            self.you = js['you']
        if self.is_stateupdate():
            self.map = js['gamestate']['map']
            self.you = js['gamestate']['you']
            self.others = js['gamestate']['others']

    def await_first_stateupdate_message(self,client):
        self.await_startofround_message(client)
        first_stateupdate = client.fetch_data()
        self.parse_message(first_stateupdate)
         
    def is_dead(self):
        return self.type == 'dead'
    def is_welcome(self):
        return self.type == 'welcome'
    def is_stateupdate(self):
        return self.type == 'stateupdate'
    def await_startofround_message(self, client):
        while not self.is_startofround():
            json_msg = client.fetch_data()
            self.parse_message(json_msg)
    def is_startofround(self):
        return self.type == 'startofround'
    def is_endofround(self):
        return self.type == 'endofround'
