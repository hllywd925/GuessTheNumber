import json
import packer
from db_controller import DBController


class ServerUser:
    def __init__(self, server, clientsocket):
        self.online = False
        self.name = None
        self.user_id = None
        self.server = server
        self.clientsocket = clientsocket
        self.db = DBController()
        self.guess = None
        self.diff = None

    def incoming_data(self):
        while self.online:
            try:
                package = self.clientsocket.recv(1024)
                package = package.decode()
                self.distributor(package)

            except ConnectionResetError:
                self.clientsocket.close()
                for idx, client in enumerate(self.server.userlist):
                    if client.clientsocket == self.clientsocket:
                        self.server.userlist.pop(idx)
                        client.shutdown()

    def distributor(self, package):
        data = json.loads(package)
        if data['typ'] == 'MSG':
            if not self.server.gameruns:
                p = packer.Packer('BCMSG', data['user_id'], data['name'], data['data'])
                p = p.pack()
                self.server.broadcast(p)
            if self.server.gameruns:
                try:
                    guess = int(data['data'])
                    if not self.guess:
                        self.guess = guess
                        self.server.game.guesses += 1
                        p = packer.Packer('SERVERMSG', 'SERVER', 'SERVER', str(guess))
                        p = p.pack()
                        self.server.privatcast(self.clientsocket, p)
                    else:
                        p = packer.Packer('SERVERMSG', 'SERVER', 'SERVER', 'Bereits geraten')
                        p = p.pack()
                        self.server.privatcast(self.clientsocket, p)
                except:
                    p = packer.Packer('SERVERMSG', 'SERVER', 'SERVER', 'Bitte eine Zahl eingeben.')
                    p = p.pack()
                    self.server.privatcast(self.clientsocket, p)

        if data['typ'] == 'LGIN':
            user_id, data_new, access = self.db.login_check(data['name'], data['data'])
            p = packer.Packer('SERVERLOGIN', user_id, data['name'], data_new)
            p = p.pack()
            self.server.privatcast(self.clientsocket, p)
            if access:
                self.user_id = user_id
                self.name = data['name']
                self.server.userlist.append(self)
            if not access:
                self.shutdown()

        if data['typ'] == 'RGSTR':
            user_id_new, name_new, passwort_new, data_new, access = self.db.creating_new_user(data['data'])
            p = packer.Packer('SERVERREGISTER', user_id_new, name_new, data_new)
            p = p.pack()
            self.server.privatcast(self.clientsocket, p)
            if access:
                self.user_id = user_id_new
                self.name = name_new
            if not access:
                self.shutdown()

        if data['typ'] == 'GMSTRT':
            p = packer.Packer('GAMERUNS', 'Server', 'Server',
                              'Guess the Number\nBitte gebe eine Zahl zwischen 1 und 100 ein.')
            p = p.pack()
            self.server.broadcast(p)
            self.server.start_gtn()

        if data['typ'] == 'UL':
            for u in self.server.userlist:
                print(f'User: {u.name}')

    def wellcome(self):
        pass

    def shutdown(self):
        self.clientsocket.close()
        self.online = False
