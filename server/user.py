
class User:

    def __init__(self):
        self.nick = None
        self.sock = None
        self.addr = None
        self.opponent = None
        self.opponent_socket = None
        self.last_msg = "".encode('utf-8')
        self.is_new_msg = False
        self.color = None