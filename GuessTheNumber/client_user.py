from client_ui import ClientUI
from client_network import Network
import packer
import json


class ClientUser:
    def __init__(self):
        self.ui = ClientUI(self)
        self.network = Network(self)
        self.user_id = None
        self.name = None
        self.passwort = None
        self.gameruns = False  # True == Spielläuft

    def try_login(self):  # sendet logininformationen
        self.packer('LGIN', self.passwort)

    def register_new_user(self):  # sendet neue Benutzerdaten
        self.packer('RGSTR', (self.name, self.passwort))

    def start_gtn(self):  # startes das GTN
        if not self.gameruns:
            self.packer('GMSTRT', '')
        else:
            self.ui.print_to_window('Spiel läuft bereits')

    def packer(self, typ, data):  # hier werden die raus gehenden JSON gepackt und an den Server gesendet
        p = packer.Packer(typ, self.user_id, self.name, data)
        p = p.pack()
        self.network.outgoing_data(p)

    def distributor(self, package):  # hier werden die rein kommenden JSON entpackt und weitergeleitet
        data = json.loads(package)
        d_typ, d_user_id, d_name, d_data = data['typ'], data['user_id'], data['name'], data['data']
        if d_typ == 'BCMSG':  # Broadcastmessage
            self.ui.print_to_window(f'[{d_name}][{d_user_id}]: {d_data}')
        if d_typ == 'SERVERMSG':
            self.ui.print_to_window(d_data)
        if d_typ == 'SERVERLOGIN':
            if d_data != 'ACCESS GRANTED':
                self.ui.print_to_window(d_data)
                self.shutdown()
            else:
                self.ui.print_to_window(f'Willkommen {self.name}!')
                self.name = d_name
                self.user_id = d_user_id
        if d_typ == 'SERVERREGISTER':
            if d_data != 'NEW USER CREATED':
                self.ui.print_to_window(d_data)
                self.shutdown()
            else:
                self.name = d_name
                self.user_id = d_user_id
                self.ui.print_to_window(f'Benutzer: {d_name} wurde erstellt.')
        if d_typ == 'GAMERUNS':  # teilt mit, dass das spiel jetzt läuft
            self.gameruns = True
            self.ui.print_to_window(f'{d_data}')
        if d_typ == 'ENDGAME':  # teilt das Ende des Spiels mit
            self.gameruns = False
            self.ui.print_to_window(d_data)

    def shutdown(self):
        self.network.serversocket.close()
        self.user_id = None
        self.name = None
        self.passwort = None
        self.network.online = False


if __name__ == "__main__":
    client = ClientUser()
    client.ui.hauptfenster()
