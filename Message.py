from enum import Enum


class Type(Enum):
    LOGIN = 0
    MOVE = 1
    CHAT_TO_ALL = 2
    CHAT_TO_OPPONENT = 3


class MyMessage:
    def __init__(self, loginFrom, type, data):
        self.loginFrom = loginFrom
        self.type = type
        self.data = data
