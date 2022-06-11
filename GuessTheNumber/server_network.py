import socket
import threading
import packer
from server_user import ServerUser
from server_gtn import GuessTheNumber


class Server(threading.Thread):
    def __init__(self):
        super().__init__()
        self.online = True
        self.gameruns = False
        self.game = None  #
        self.address = '127.0.0.1'
        self.port = 5555
        self.serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.userlist = []

    def awake(self):
        self.serversocket.bind((self.address, self.port))
        self.serversocket.listen(0)
        print('Server gestartet...')

        while self.online:
            (clientsocket, addr) = self.serversocket.accept()

            user = ServerUser(self, clientsocket)
            user.online = True

            new_thread = threading.Thread(target=user.incoming_data, args=())
            new_thread.start()

    def broadcast(self, data):
        for user in self.userlist:
            d = data.encode()
            user.clientsocket.send(d)

    def privatcast(self, clientsocket, data):
        d = data.encode()
        clientsocket.send(d)

    def update_userlist(self):
        pass

    def start_gtn(self):
        if not self.gameruns:
            self.game = GuessTheNumber(self, self.userlist)
            game_thread = threading.Thread(target=self.game.start, args=())
            game_thread.start()
            self.gameruns = True
        else:
            print('Spiel bereits gestartet!')

    def end_gtn(self, gesucht, gewinner, diff):
        self.gameruns = False  # setzt Gamestatus zurück
        for u in self.userlist:  # setzt Schätzung zurück
            u.guess = None
            u.diff = None
        p = packer.Packer('ENDGAME', '', '', f'{gewinner} gewinnt mit seinem Tipp: {diff}\nGesucht war: {gesucht}')  # teilt den Clients das Spielende mit
        p = p.pack()
        self.broadcast(p)

    def shutdown(self):
        for client in self.userlist:
            client.shutdown()
        self.online = False
        self.serversocket.close()


if __name__ == "__main__":
    s = Server()
    s.awake()
