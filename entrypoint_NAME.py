from util.Client import Client
if __name__ == '__main__':
    bot_name = b"NAME bbb\n" # <--- bot name goes here
    c = Client(bot_name)
    #TODO need a while true here or something to setup and run the bot FOR ALL
    #THE ROUNDS :O
    c.setup_bot()
    c.run_bot()