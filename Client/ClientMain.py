import pickle
from tkinter import Tk, Canvas, BOTH, Menu, Entry, Label, Button
from socket import *
from Message import MyMessage, Type


class ClientMain:
    def __init__(self):
        self.host = '127.0.0.1'
        self.port = 7777
        self.addr = (self.host, self.port)
        self.socket = socket(AF_INET, SOCK_STREAM)
        self.connect()
        self.makeWindow()

    def connect(self):
        self.socket.connect(self.addr)

    def logIn(self):
        login = self.loginEntery.get()
        password = self.passwordEntery.get()
        m = MyMessage(login, Type.LOGIN, (login, password))
        data = pickle.dumps(m)
        self.socket.send(data)

    def makeWindow(self):
        window = Tk()
        window.title("Добро пожаловать в приложение PythonRu")
        mainmenu = Menu(window)
        window.geometry('480x640')
        lbl = Label(window, text="                                             ")
        lbl.grid(column=0, row=0)
        l1 = Label(window, text="Логин")
        l1.grid(column=0, row=1)
        l1 = Label(window, text="Пароль")
        l1.grid(column=0, row=2)
        self.loginEntery = Entry(window, width=10)
        self.loginEntery.grid(column=1, row=1)
        self.passwordEntery = Entry(window, width=10)
        self.passwordEntery.grid(column=1, row=2)
        #def fce(x=loginEntery.get(), y=passwordEntery.get()):
        #    self.logIn(x, y)
        btn = Button(window, text="Войти", command=self.logIn)
        btn.grid(column=2, row=0)
        print("Window done")
        window.mainloop()


if __name__ == "__main__":
    c = ClientMain()
