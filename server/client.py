from socket import *
import time
import threading
host = '192.168.88.165'
port = 777
addr = (host,port)
class Client:

    def __init__(self):
        self.is_working = True
        self.nickname = None
        self.color = None
        self.socket = socket(AF_INET, SOCK_STREAM)
        self.socket.connect(addr)
        self.opponent = None
        self.oppsock = socket()
        self.start()

    def start(self):

        self.nickname = input('your name: ')
      #  self.nickname = self.nickname.encode('utf-8')
        self.socket.send(self.nickname.encode('utf-8'))

        msg = self.socket.recv(1024)
        print(msg.decode('utf-8'))

        self.opponent = input ('your opponent: ')
       # self.opponent =  self.opponent.encode('utf-8')
        self.socket.send(self.opponent.encode('utf-8'))

        msg = self.socket.recv(1024)
        print(msg.decode('utf-8'))

        self.color = input('your color (1 is white and -1 is black): ')
      #  self.color = self.opponent.encode('utf-8')
        self.socket.send(self.color.encode('utf-8'))


        #   !socket of your opponet!
        self.oppsock = self.socket.recv(1024)
        print(self.oppsock.decode('utf-8'))




        time.sleep(0.3)
        self.threading_my_func()

    def threading_my_func(self):
      #  thrsend = threading.Thread(target=self.sending)
        thrreceiving = threading.Thread(target=self.receiving)
       # thrsend.start()
        thrreceiving.start()

    def sending(self, msg):

        #msg = input()
        msg = msg.encode('utf-8')
        self.socket.send(msg)


    def receiving(self):
        while self.is_working:
            msg = self.socket.recv(1024).decode('utf-8')
            print(msg)
            yield msg

if __name__ == '__main__':
    cl = Client()
