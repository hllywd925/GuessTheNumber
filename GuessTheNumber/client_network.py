import socket
from threading import Thread


class Network:
    def __init__(self, parent):
        self.parent = parent
        self.online = False
        self.server = '127.0.0.1'
        self.port = 5555
        self.serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connecting(self, log_or_reg):
        self.serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.serversocket.connect((self.server, self.port))

            new_thread = Thread(target=self.incoming_data, args=())
            self.online = True
            new_thread.start()
            if log_or_reg == 'log':
                self.parent.try_login()
            if log_or_reg == 'reg':
                self.parent.register_new_user()

        except OSError as e:
            self.parent.ui.print_to_window(e)

    def outgoing_data(self, package):
        if self.online:
            p = package.encode()
            self.serversocket.send(p)

    def incoming_data(self):
        while self.online:
            try:
                package = self.serversocket.recv(1024)
                package = package.decode()
                self.parent.distributor(package)

            except ConnectionAbortedError as e:
                print(e)
                self.parent.shutdown()
