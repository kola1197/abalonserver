import socket
from user import User
import threading
import time


class Server:

    def __init__(self):
        self.daemon = True
        self.is_connected = True
        self.dict = {}  # cловарь имя пользователя - имя сокета
        self.clients = []
        self.nicknames = []

        #self.last_msg = "".encode('utf-8')
        self.serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("server initialised")
        self.start()
        # conn, addr = self.serv.accept()
        #  threading.Thread(target=self.connecting(conn, addr)).start()

        threading.Thread(target=self.accepting()).start()

    def start(self):
        host = '192.168.88.165'
        port = 777
        self.serv.bind((host, port))
        self.serv.listen(10)
        print('start')

    def accepting(self):
        while True:
            print("waiting")
            conn, addr = self.serv.accept()
            t = threading.Thread(target=self.connecting, args=(conn, addr, ), name='daemon', daemon=True)
            print("start")
            t.start()

    def connecting(self, conn, addr):  # подключение новых пользователей

        print(conn)
        print(addr)

        if addr not in self.clients:
            #thrconn = threading.Thread(target=self.meetings(addr, conn))
            #thrconn.start()
            self.meetings(addr, conn)
            print('meeting ended')
        else:
            conn.close()
            self.is_connected = False

    def sending(self, user):
        while self.is_connected:
            if user.is_new_msg == True:
                user.opponent_socket.send(user.last_msg)
                user.is_new_msg = False

    def receiving(self, user):
        while self.is_connected:
            user.last_msg = user.sock.recv(1024)
            user.is_new_msg = True
            time.sleep(0.08)
            msg = 'delivered at ' + time.ctime() + '  ---->  ' + user.last_msg.decode('utf-8')
            # self.send_to_client(user.sock, 'Me: '+ msg)
            self.print_on_server(('from ' + user.nick + " to " + user.opponent + ' : ' + msg).encode('utf-8'))

    def meetings(self, addr, conn):

        user = User()

        # meetings: name and opponent's name

        nickname = conn.recv(1024)
        nickname = nickname.decode('utf-8')

        print(nickname + ' присоединился')
        msg = 'connected!'
        self.send_to_client(conn, msg)

        self.clients.append(addr)
        self.nicknames.append(nickname)
        self.dict.update({nickname: conn})

        opponent = conn.recv(1024)
        opponent = opponent.decode('utf-8')





        user.addr = addr
        user.sock = conn
        user.nick = nickname
        user.opponent = opponent

        print(opponent + ' - имя соперника участника ' + nickname)

        if opponent in self.nicknames:
            msg = opponent + ' connected'
            self.send_to_client(user.sock, msg)
            # сокет соперника
            msg = self.dict.get(opponent)
            user.opponent_socket = msg
            self.send_to_client(user.sock, msg)
            self.threads(user)
            print(user.nick + ' ------ threads open')
            color = conn.recv(1024)
            color = color.decode('utf-8')

            user.color = color

        else:
            msg = opponent + ' is not here :('
            self.send_to_client(user.sock, msg)

    def threads(self, user):
        thrsend = threading.Thread(target=self.sending, args=(user,))
        thrsend.start()

        thrreceiving = threading.Thread(target=self.receiving, args=(user,))
        thrreceiving.start()

    def print_on_server(self, data):
        print(data.decode('utf-8'))

    def send_to_client(self, client_socket, msg):
        client_socket.send(str(msg).encode('utf-8'))


if __name__ == '__main__':
    s = Server()
