from enum import Enum
from tkinter import *
from Board import *
from Point import*

class Color(Enum):
    black = -1
    white = 1

class Ball:

    def __init__(self, color):
        self.color = color
        self.coord = Point(-1, -1)

    def __init__(self, color, x, y):
        self.color = color
        self.coord = Point(x, y)

    def set_point(self, x, y):
        self.coord.X = x
        self.coord.Y = y
