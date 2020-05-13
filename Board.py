from Ball import *
from tkinter import *
from Logger import Logger

class Board:

    def __init__(self):
        self.Logger=Logger()
        self.balls = []
        self.draw_array = []
        self.fill()
        self.white_is_move=1
        self.white=14
        self.black=14
        self.cmove=0
        self.num = [[0 for i in range(j)] for j in range(5, 10)] + [[0 for i in range(13 - j)] for j in range(5, 9)]
        for i in range(5):
            for j in range(9 - i):
                self.num[i + 4][j] = i + j
        for i in range(4):
            for j in range(8 - i):
                self.num[3 - i][j] = j


    def fill(self):
        for i in range(5):
            b = Ball(-1, i, 0)
            self.balls.append(b)
        for i in range(6):
            b = Ball(-1, i, 1)
            self.balls.append(b)
        for i in range(3):
            b = Ball(-1, i+2, 2)
            self.balls.append(b)
        for i in range(5):
            b = Ball(1, i, 8)
            self.balls.append(b)
        for i in range(6):
            b = Ball(1, i, 7)
            self.balls.append(b)
        for i in range(3):
            b = Ball(1, i+2, 6)
            self.balls.append(b)

    def update_draw_array(self):
        self.draw_array = [[0 for i in range(j)] for j in range(5, 10)] + [[0 for i in range(13 - j)] for j in range(5, 9)]
        for b in self.balls:
            self.draw_array[b.coord.Y][b.coord.X] = b.color
     #   self.draw_in_console()

    def draw_in_console(self):
        print(self.draw_array)

    def count(self):
        self.white = 0
        self.black = 0
        for list in self.draw_array:
            for color in list:
                if color == 1:
                    self.white += 1
                if color == -1:
                    self.black += 1