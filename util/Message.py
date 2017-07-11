import json
class Message(object):
    def __init__(self):
        self.type = ''
        self.map = None

    def __init__(self, json_message):
        self.__init__()
        parse_message(json_message)

    def parse_message(self, json_message):
        js = json.loads(json_message.decode())
        self.type = js['messagetype']
        print(self.type)
        print("TODO parse needs finishing/Testing!")
        self.map = js['map']

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