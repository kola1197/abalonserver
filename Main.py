from tkinter import *
from Board import *
from math import atan2, degrees
from Logger import Logger
from time import sleep
import easygui
import os
from server.client import Client
path = os.getcwd()+"\\image\\"
root = Tk()
mainmenu = Menu(root)
root.config(menu=mainmenu)


canv = Canvas()
canv.pack(fill=BOTH, expand=1)
button_size = 83
subs=75
subs1=2
black = PhotoImage(file=path+"black.png")
black = black.subsample(subs)
white = PhotoImage(file=path+"white.png")
white = white.subsample(subs)
none = PhotoImage(file=path+"none.png")
none = none.subsample(subs)
but1 = PhotoImage(file=path+"But1.png")
but1 = but1.subsample(subs1)
but2 = PhotoImage(file=path+"But2.png")
but2 = but2.subsample(subs1)
but3 = PhotoImage(file=path+"But3.png")
but3 = but3.subsample(subs1)
but4 = PhotoImage(file=path+"But4.png")
but4 = but4.subsample(subs1)
but5 = PhotoImage(file=path+"But5.png")
but5 = but5.subsample(subs1)
but6 = PhotoImage(file=path+"But6.png")
but6 = but6.subsample(subs1)
yellow_white = PhotoImage(file=path+"whiteact.png")
yellow_white = yellow_white.subsample(subs)
yellow_black = PhotoImage(file=path+"blackact.png")
yellow_black = yellow_black.subsample(subs)

root.geometry('1000x1000')
host = '192.168.88.165'
port = 777
addr = (host, port)

class Main:
    def __init__(self):
        self.buttons = [[0 for i in range(j)] for j in range(5, 10)] + [[0 for i in range(13 - j)] for j in range(5, 9)]
        self.selected = []
        self.pushed = []
        self.l = Label()
        self.counter1 = Label()
        self.counter2 = Label()
        self.board = Board()
        self.board.Logger.Write("initialisation done")

        self.client = Client()



    def move_restart(self):      #сброс хода
        self.selected.clear()
        self.update()

    def to_pixels(self, x, y): #cell's coord to pixels

        x = 293 + button_size * x - y * button_size / 2
        y = 205 + y * button_size
        self.board.Logger.Write((x, y))
        return x, y

    def make_it_yellow(self):         #выделение шарика
        for ball in self.selected:
            n = self.board.num[ball[0]].index(ball[1])
            m = self.board.draw_array[ball[0]][n]
            if m == 1 and self.board.white_is_move == 1:
                self.update()
            elif m == -1 and self.board.white_is_move == -1:
                self.update()
            else:
                self.move_restart()

    def tap(self, X, Y):    # обработка нажатий на клетки
        var = self.selected
        deleg = self.make_it_yellow
        deleg1 = self.update

        def wrapper(v=var, x=X, y=Y, delegat=deleg, delegat1=deleg1):
            if len(var) >= 3:
                self.move_restart()
            if [x, y] not in var:
                var.append([x, y])
                delegat()
                self.make_it_yellow()
            elif [x, y] in var:
                var.remove([x, y])
                delegat()
                delegat1()

        return wrapper  # проверить цвет нужного нам шарика

    def get_color(self, ball, x, y):        #определение цвета шарика по его координатам на поле
        if 0 <= ball[0] <= 8:
            if ball[1] in self.board.num[ball[0]]:
                n = self.board.num[ball[0]].index(ball[1])
                return self.board.draw_array[ball[0]][n]
            else:
                return 'out'
        else:
            return 'out'

    def simple_move(self, x, y): # ход только своими фишками
        for ball in self.selected: # заменяю выделенные клетки на пустые
            n = self.board.num[ball[0]].index(ball[1])
            self.board.draw_array[ball[0]][n] = 0
        for ball in self.selected:  # меняю цвета с учетом сдвига на цвет хода
            m = self.board.num[ball[0] + x].index(ball[1] + y)
            self.board.draw_array[ball[0] + x][m] = self.board.white_is_move

       # self.board.white_is_move = - self.board.white_is_move ###потому что клиент!
        self.move_restart()
        self.board.Logger.WriteGameInfo(self.board.draw_array)

######################клиентское
        self.client.sending(str(self.board.draw_array))

        board = self.client.receiving()
        for a in board:
            d = self.deskarray_from_str_to_tuple(a)
            d= [ list(d[i]) for i in range(9) ]

            break

        self.board.draw_array = d
        print(self.board.draw_array)
        self.update()


        self.board.cmove+=1
            # тут мы двигаем шарики соперника

    def move(self, x, y):     # сдвиг шариков противника
        self.board.Logger.Write('after i will push')
        for ball in self.pushed:
            n = self.board.num[ball[0]].index(ball[1])
            self.board.draw_array[ball[0]][n] = 0
        for ball in self.pushed:
            m = self.board.num[ball[0]].index(ball[1])
            self.board.draw_array[ball[0]][m] = - self.board.white_is_move

        self.update()
        self.board.Logger.Write(str(self.pushed) + '.. pushed to')
        self.pushed.clear()

    def next_cell(self, x, y):  # проверка следующих клеток после выделенных в направлении хода
        if len(self.selected) == 1:
            for ball in self.selected:
                nball = [ball[0] + x, ball[1] + y]
                if self.get_color(nball, x, y) == 0:
                    self.simple_move(x, y)
                else:
                    self.board.Logger.Write('wrong move')
                    self.move_restart()
        elif len(self.selected) == 2:
            new = []
            for ball in self.selected:
                new.append([ball[0] + x, ball[1] + y])
            for ball in new:
                if ball not in self.selected:
                    if self.get_color(ball, x, y) == 0:
                        self.simple_move(x, y)
                        break
                    elif self.get_color(ball, x, y) == -self.board.white_is_move:
                        nball = [ball[0] + x, ball[1] + y]
                        self.pushed.append(nball)
                        if self.get_color(nball, x, y) == 0:
                            self.move(x, y)
                            self.simple_move(x, y)
                        elif self.get_color(nball, x, y) == 'out':
                            self.simple_move(x, y)
                            self.pushed.clear()
                        else:
                            self.move_restart()
                    else:
                        self.move_restart()
        elif len(self.selected) == 3:
            new = []
            for ball in self.selected:
                new.append([ball[0] + x, ball[1] + y])
            for ball in new:
                if ball not in self.selected:
                    if self.get_color(ball, x, y) == 0:
                        self.board.Logger.Write('3 balls and the next cell is empty')
                        self.simple_move(x, y)

                        break
                    elif self.get_color(ball, x, y) == -self.board.white_is_move:
                        n2ball = [ball[0] + x, ball[1] + y]
                        self.pushed.append(n2ball)
                        if self.get_color(n2ball, x, y) == 0:
                            self.move(x, y)
                            self.simple_move(x, y)
                            break
                        elif self.get_color(n2ball, x, y) == 'out':
                            self.simple_move(x, y)
                            self.pushed.clear()
                        elif self.get_color(n2ball, x, y) == -self.board.white_is_move:
                            n3ball = [n2ball[0] + x, n2ball[1] + y]
                            self.pushed.append(n3ball)

                            if self.get_color(n3ball, x, y) == 0:
                                self.move(x, y)
                                self.simple_move(x, y)
                                break
                            elif self.get_color(n3ball, x, y) == 'out':
                                self.simple_move(x, y)
                                self.pushed.clear()
                            else:
                                self.move_restart()
                        else:
                            self.move_restart()
                    else:
                        self.move_restart()

                        # нужно проверить перед move, что цвет массива совпадает c white_is_move (что ваш ход)

    def check_color(self, x, y):   # проверка, ваш ли ход
        ball = self.selected[0]
        if self.get_color(ball, x, y) == self.board.white_is_move:
            self.next_cell(x, y)
        else:
            self.move_restart()

    def check_color_and_next_not_other_colored(self, x, y):   #если несколько шариков в ряд и они идут по прямой, отличной от той, на которой лежат
        ball = self.selected[0]
        if self.get_color(ball, x, y) == self.board.white_is_move:
            for ball in self.selected:
                ball = [ball[0] + x, ball[1] + y]
                if self.get_color(ball, x, y) != 0:
                    self.move_restart()
                    break
            self.next_cell(x, y)
        else:
            self.move_restart()

    def go_to(self, X, Y):   # передаю вектор хода и проверяю, правильно ли относительно друг друга расположны шарики, вызываю другие проверки корректности зода

        var = self.selected
        var2 = self.check_color  # куча проверок корректности хода
        var3 = self.check_color_and_next_not_other_colored

        def wrapper(v=var, x=X, y=Y, check_color=var2, check_color_and_next_not_other_colored=var3):
            colors = []
            for ball in var:  # все ли выделенные шарики одного цвета?
                n = self.board.num[ball[0]].index(ball[1])
                m = self.board.draw_array[ball[0]][n]
                colors.append(m)
                if 0 <= ball[0] + x <= 8:
                    a = self.board.num[ball[0] + x]
                    if ball[1] + y in a:  # рядом ли выбранные шарики и не противоречат ли направлению
                        if len(var) == 1:
                            check_color(x, y)
                        elif len(var) == 2:
                            if var[0][0] == var[1][0] and abs(var[0][1] - var[1][1]) == 1 and x == 0:
                                check_color(x, y)
                            elif abs(var[0][0] - var[1][0]) == 1 and var[0][1] == var[1][1] and y == 0:
                                check_color(x, y)
                            elif abs(var[0][0] - var[1][0]) == 1 and abs(var[0][1] - var[1][1]) == 1 and abs(
                                    x) == 1 and abs(y) == 1:
                                check_color(x, y)
                            elif var[0][0] == var[1][0] and abs(var[0][1] - var[1][1]) == 1 and x != 0:
                                check_color_and_next_not_other_colored(x, y)
                            elif abs(var[0][0] - var[1][0]) == 1 and var[0][1] == var[1][1] and y != 0:
                                check_color_and_next_not_other_colored(x, y)
                            elif abs(var[0][0] - var[1][0]) == 1 and abs(var[0][1] - var[1][1]) == 1 and (
                                    abs(x) == 1 and abs(y)) != 1:
                                check_color_and_next_not_other_colored(x, y)

                        elif len(var) == 3:
                            xs = [var[0][0], var[1][0], var[2][0]]
                            ys = [var[0][1], var[1][1], var[2][1]]
                            if max(xs) == min(xs) and max(ys) - min(ys) == 2 and x == 0:
                                check_color(x, y)
                            elif max(xs) - min(xs) == 2 and max(ys) == min(ys) and y == 0:
                                check_color(x, y)
                            elif max(xs) - min(xs) == 2 and max(ys) - min(ys) == 2 and abs(x) == 1 and abs(y) == 1:
                                check_color(x, y)
                            elif max(xs) == min(xs) and max(ys) - min(ys) == 2 and x != 0:
                                check_color_and_next_not_other_colored(x, y)
                            elif max(xs) - min(xs) == 2 and max(ys) == min(ys) and y != 0:
                                check_color_and_next_not_other_colored(x, y)
                            elif max(xs) - min(xs) == 2 and max(ys) - min(ys) == 2 and not (
                                    abs(x) == 1 and abs(y) == 1):
                                check_color_and_next_not_other_colored(x, y)

                    else:  # не вылезаю ли за границы поля своим шариком
                        self.move_restart()
                        break
                else:
                    self.move_restart()
                    break
            if 0 in colors:
                self.move_restart()
            if 1 in colors and -1 in colors:
                self.move_restart()

        return wrapper

    def draw_buttons(self):   # отрисовка кнопок под шарики
        for i in range(5):
            for j in range(9 - i):
                b = Button(root, activebackground='blue', relief=FLAT, command=self.tap(4 + i, i + j))
                b.place(x=button_size + i * button_size / 2 + button_size * j,
                        y=button_size + i * button_size + button_size * 5)
                self.buttons[i + 4][j] = b
                b.bind('<Button-3>', self.coord(1, 4 + i, i + j))
        for i in range(4):
            for j in range(8 - i):
                b = Button(root, activebackground='blue', relief=FLAT, command=self.tap(3 - i, j))
                b.place(x=1.5 * button_size + i * button_size / 2 + button_size * j,
                        y=-i * button_size + button_size * 5)
                self.buttons[3 - i][j] = b
                b.bind('<Button-3>', self.coord(1, 3 - i, j))

        self.update()

    def new_game(self): # новая игра

        self.board = Board()
        self.board.update_draw_array()
        m.draw_buttons()
        self.board.Logger.WriteGameInfo(self.board.draw_array)
        self.l.config(text="White's turn")
        self.l.pack()
        self.counter1.config(text='white: ' + str(self.board.white))
        self.counter2.config(text='black: ' + str(self.board.black))
        self.counter1.pack()
        self.counter2.pack()
       # self.board.white_is_move = self.client.color
        # графика

    def check_win(self):
        if self.board.white == 8:
            easygui.msgbox('Победили черные!')
            root.update()
            self.board.Logger.createGameInfoPath()
            self.board.Logger.createLogFile()
            self.pushed.clear()
            sleep(1)
            self.new_game()
        elif self.board.black == 8:
            easygui.msgbox('Победили белые!')
            root.update()
            self.board.Logger.createGameInfoPath()
            self.board.Logger.createLogFile()
            self.pushed.clear()
            sleep(1)
            self.new_game()

    def update(self, *desk):  # обновление графики
        if desk!=():
            desk = [list(i) for i in desk]
            self.board.draw_array=desk
            self.selected.clear()
            sleep(0.7)
            self.board.white_is_move = - self.board.white_is_move
        self.board.count()
        for i in range(len(self.buttons)):
            for j in range(len(self.buttons[i])):
                if self.board.draw_array[i][j] == 1:
                    self.buttons[i][j].config(image=white)
                elif self.board.draw_array[i][j] == -1:
                    self.buttons[i][j].config(image=black)
                else:
                    self.buttons[i][j].config(image=none)

        if self.board.white_is_move == 1:
            self.l.config(text="White's turn")
        else:
            self.l.config(text="Black's turn")
        for ball in self.selected:
            n = self.board.num[ball[0]].index(ball[1])
            m = self.board.draw_array[ball[0]][n]
            if m == 1 and self.board.white_is_move == 1:
                self.buttons[ball[0]][n].config(image=yellow_white)
            elif m == -1 and self.board.white_is_move == -1:
                n = self.board.num[ball[0]].index(ball[1])
                self.buttons[ball[0]][n].config(image=yellow_black)
        self.l.pack()
        self.counter1.config(text='white: ' + str(self.board.white))
        self.counter2.config(text='black: ' + str(self.board.black))
        self.counter1.pack()
        self.counter2.pack()
        self.check_win()
        root.update()

    def go_to1(self, x, y): # управление пкм

        var = self.selected
        var2 = self.check_color  # куча проверок корректности хода
        var3 = self.check_color_and_next_not_other_colored
        colors = []
        for ball in var:  # все ли выделенные шарики одного цвета?
            n = self.board.num[ball[0]].index(ball[1])
            m = self.board.draw_array[ball[0]][n]
            colors.append(m)
            if 0 <= ball[0] + x <= 8:
                a = self.board.num[ball[0] + x]
                if ball[1] + y in a:  # рядом ли выбранные шарики и не противоречат ли направлению
                    if len(self.selected) == 1:
                        self.check_color(x, y)
                    elif len(var) == 2:
                        if var[0][0] == var[1][0] and abs(var[0][1] - var[1][1]) == 1 and x == 0:
                            self.check_color(x, y)
                        elif abs(var[0][0] - var[1][0]) == 1 and var[0][1] == var[1][1] and y == 0:
                            self.check_color(x, y)
                        elif abs(var[0][0] - var[1][0]) == 1 and abs(var[0][1] - var[1][1]) == 1 and abs(
                                x) == 1 and abs(y) == 1:
                            self.check_color(x, y)
                        elif var[0][0] == var[1][0] and abs(var[0][1] - var[1][1]) == 1 and x != 0:
                            self.check_color_and_next_not_other_colored(x, y)
                        elif abs(var[0][0] - var[1][0]) == 1 and var[0][1] == var[1][1] and y != 0:
                            self.check_color_and_next_not_other_colored(x, y)
                        elif abs(var[0][0] - var[1][0]) == 1 and abs(var[0][1] - var[1][1]) == 1 and (
                                abs(x) == 1 and abs(y)) != 1:
                            self.check_color_and_next_not_other_colored(x, y)

                    elif len(var) == 3:
                        xs = [var[0][0], var[1][0], var[2][0]]
                        ys = [var[0][1], var[1][1], var[2][1]]
                        if max(xs) == min(xs) and max(ys) - min(ys) == 2 and x == 0:
                            self.check_color(x, y)
                        elif max(xs) - min(xs) == 2 and max(ys) == min(ys) and y == 0:
                            self.check_color(x, y)
                        elif max(xs) - min(xs) == 2 and max(ys) - min(ys) == 2 and abs(x) == 1 and abs(y) == 1:
                            self.check_color(x, y)
                        elif max(xs) == min(xs) and max(ys) - min(ys) == 2 and x != 0:
                            self.check_color_and_next_not_other_colored(x, y)
                        elif max(xs) - min(xs) == 2 and max(ys) == min(ys) and y != 0:
                            self.check_color_and_next_not_other_colored(x, y)
                        elif max(xs) - min(xs) == 2 and max(ys) - min(ys) == 2 and not (abs(x) == 1 and abs(y) == 1):
                            self.check_color_and_next_not_other_colored(x, y)

                else:  # не вылезаю ли за границы поля своим шариком
                    self.move_restart()
                    break
            else:
                self.move_restart()
                break
        if 0 in colors:
            self.move_restart()
        if 1 in colors and -1 in colors:
            self.move_restart()


    def vect(self, x, y, therefr):  # определяю угол наклона вектора к точку, куда нажали. Управление пкм
        a = self.selected
        if [y, x] in self.selected:
            return 0
        if therefr == 1:
            x, y = self.to_pixels(x, y)

        if len(a) == 3:

            n = a[0][0] + a[0][1]
            m = a[1][0] + a[1][1]
            k = a[2][0] + a[2][1]
            l = sorted([n, m, k])
            if n == l[1]:
                x1, y1 = self.to_pixels(a[0][1], a[0][0])
                vector = [x - x1, y - y1]
            elif m == l[1]:
                x1, y1 = self.to_pixels(a[1][1], a[1][0])
                vector = [x - x1, y - y1]

            elif k == l[1]:
                x1, y1 = self.to_pixels(a[2][1], a[2][0])
                vector = [x - x1, y - y1]

        elif len(a) == 2:
            x1 = (a[0][1] + a[0][1]) / 2
            y1 = (a[0][0] + a[1][0]) / 2
            x1, y1 = self.to_pixels(x1, y1)

            vector = [x - x1, y - y1]
        elif len(a) == 1:
            x1, y1 = self.to_pixels(a[0][1], a[0][0])
            vector = [x - x1, y - y1]
        elif len(a) == 0:
            return 0
        t = -degrees(atan2(vector[1], vector[0]))
        # определяю угол наклона вектора направления к оси х
        if -30 <= t <= 30:
            self.go_to1(0, 1)
        elif 30 <= t <= 90:
            self.go_to1(-1, 0)
        elif 90 <= t <= 150:
            self.go_to1(-1, -1)
        elif 150 <= t <= 180 or -180 <= t <= -150:
            self.go_to1(0, -1)
        elif -150 <= t <= -90:
            self.go_to1(1, 0)
        elif -90 <= t <= -30:
            self.go_to1(1, 1)

    def coord(self, Z, X, Y):  # передаю координаты клетки в формате сторока - ряд
        deleg = self.vect

        def wrapper(z=Z, x=X, y=Y, d=deleg):
            d(y, x, 1)

        return wrapper

    def deskarray_from_str_to_tuple(self, d):
        d = d[1:-1]
        d = d[0:-1]
        d = d.split(']')
        for i in range(9):
            if i > 0:
                d[i] = d[i][3:]
            else:
                d[i] = d[i][1:]
            d[i] = d[i].split(',')
            for j in range(len(d[i])):
                d[i][j] = int(d[i][j])
            d[i] = tuple(d[i])
       # d = d[:-1]
        return d


    def last(self): # предыдущий ход
        if self.board.cmove!=0:
            game=self.board.Logger.read_file(self.board.Logger.gameInfoFileName)
            self.board.cmove-=1
            i=self.board.cmove
            d = game[i]
            d = self.deskarray_from_str_to_tuple(d)
            d = d[:-1]
            self.board.Logger.line_del()
            self.update(d[0],d[1],d[2],d[3],d[4],d[5],d[6],d[7],d[8])

    def rename(self, name):
        #self.board.Logger.gameInfoFileName = name
        #namelog = 'Log'+str(name[4:])
        #self.board.Logger.logFileName = namelog
        #try:
        #    with open(name) as f:
        #        self.board.cmove= len(f.readlines())  #надо убрать перемернную в логгере одну
        #except Exception:
        #    self.board.cmove=0
        pass

    def test(self):   # просмотр старой игры
        d=self.board.Logger.directory
        v=self.board.Logger.read_file
        var=self.update
        rename=self.rename

        def wrapper(v=self.board.Logger.read_file, var=self.update, d=self.board.Logger.directory, rename=self.rename):
            name = self.board.Logger.directory()
            self.rename(name)
            var=self.update
            desk=self.board.Logger.read_file(name)
            for d in desk:
                d=d[1:-1]
                d=d[0:-1]
                d = d.split(']')
                for i in range(9):
                    if i > 0 :
                        d[i] = d[i][3:]
                    else:
                        d[i] = d[i][1:]
                    d[i] = d[i].split(',')
                    for j in range(len(d[i])):
                        d[i][j]=int(d[i][j])
                    d[i]=tuple(d[i])
                d=d[:-1]
                print(d)
                self.update(d[0],d[1],d[2],d[3],d[4],d[5],d[6],d[7],d[8])

        return wrapper

    def dir(self, event): # координаты нажатия вне поля
        x = event.x
        y = event.y
        self.vect(x, y, 0)

    def last_move(self):
        l=self.last
        def wrapper(l=self.last):
            self.last()
        return wrapper
    # def direction(self, event):
    #     X=event.x
    #     Y=event.y
    #     func=self.draw_direction
    #     def wrapper(x=X, y=Y, func=self.draw_direction):
    #         self.draw_direction(x,y)
    #
    #     return wrapper


    # def draw_direction(self,x,y):
    #     [x,y]=self.vect(x,y, 'draw')
    #     print([x,y])
if __name__ == "__main__":
    m = Main()

    #start = Button(text='Новая игра', command=m.new_game)
    #start.place(x=100, y = 225)
    root.bind('<w>', m.go_to(-1, -1))
    root.bind('<e>', m.go_to(-1, 0))
    root.bind('<d>', m.go_to(0, 1))
    root.bind('<x>', m.go_to(1, 1))
    root.bind('<z>', m.go_to(1, 0))
    root.bind('<a>', m.go_to(0, -1))
    canv.bind('<Button-3>', m.dir)
    #canv.bind('<Motion>', m.direction)
    # выбор направления
    up1 = Button(text='-', image=but1, relief=FLAT, command=m.go_to(-1, -1))
    up1.place(x=870, y=700)
    down1 = Button(text='-', image=but5, relief=FLAT, command=m.go_to(1, 0))
    down1.place(x=870, y=800)
    left = Button(text='-', image=but4, relief=FLAT, command=m.go_to(0, -1))
    left.place(x=850, y=750)
    right = Button(text='-', image=but3, relief=FLAT, command=m.go_to(0, 1))
    right.place(x=940, y=750)
    up2 = Button(text='-', image=but2, relief=FLAT, command=m.go_to(-1, 0))
    up2.place(x=920, y=700)
    down2 = Button(text='-', image=but6, relief=FLAT, command=m.go_to(1, 1))
    down2.place(x=920, y=800)



    def info():
        easygui.msgbox('''
Прежде нужно выделить шарики, которыми вы будете ходить. Затем нужно выбрать направление, есть три способа:
Управление кнопками WEDXZA
Нажать ПКМ в том направлении, куда хотите походить относительно среднего шарика
Кнопки со стрелочками на поле
Чтобы продолжить старую партию, нужно выбрать файл из папки gameInfo
        ''')
    def rules():
        easygui.msgbox('''
Вы можете выделять шарики только на одной прямой.
Вы можете выделить от 1 до 3 шариков одного цвета
Вы можете выбрать направление так, чтобы либо шарик попал на пустую клетку, 
либо большее количество ваших шариков толкнуло меньшее количество шариков противника.
(2 против 1, 3 против 1 и 2)
Цель: вытолкнуть 8 шариков противника.
        ''' )

    mainmenu.add_command(label='Новая игра', command=m.new_game)
    mainmenu.add_command(label='Отмена хода', command=m.last_move())
    mainmenu.add_command(label='Правила игры',command=rules)
    mainmenu.add_command(label='Управление', command=info)
    mainmenu.add_command(label='Продолжить старую партию', command=m.test())

root.mainloop()
