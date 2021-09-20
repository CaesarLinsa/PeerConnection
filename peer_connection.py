import selectors
import socket
import threading
import time
import argparse


client_connections = {}
server_connections = {}


def get_another_by_client(point):
    while True:
        if client_connections.get(point):
            return client_connections.get(point)
        else:
            time.sleep(1)


def get_another_by_server(point):
    while True:
        if server_connections.get(point):
            return server_connections.get(point)
        else:
            time.sleep(1)


class Client(threading.Thread):

    def __init__(self, c_host, c_port):
        self.c_addr = (c_host, c_port)
        self.cli = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.cli.connect(self.c_addr)
        super(Client, self).__init__()

    def run(self):
        while True:
            data = self.cli.recv(1024)
            if data:
                if get_another_by_client(self.cli).fileno != -1:
                    get_another_by_client(self.cli).send(data)
            else:
                if client_connections.get(self.cli):
                    s = client_connections.pop(self.cli)
                    if server_connections.get(s):
                        server_connections.pop(s)
                self.cli.close()


class Server(threading.Thread):
    """
    用户连接server， server数据转发给client， 由client连接目标机器，
    实现用户访问目标机器
    """
    def __init__(self, host, port, c_host, c_port=22):
        super(Server, self).__init__()
        self.server_addr = (host, port)
        self.c_host = c_host
        self.c_port = c_port
        self.sel = selectors.DefaultSelector()

    def read(self, conn, mask):
        data = conn.recv(1024)
        if data:
            print('conn', get_another_by_server(conn))
            get_another_by_server(conn).send(data)
        else:
            print('closing', conn)
            self.sel.unregister(conn)
            cli = server_connections.pop(conn)
            client_connections.pop(cli)
            conn.close()

    def accept(self, sock, mask):
        conn, addr = sock.accept()
        print('connected %s from %s' % (self.server_addr, str(addr)))
        conn.setblocking(False)
        c = Client(self.c_host, self.c_port)
        c.start()
        server_connections[conn] = c.cli
        client_connections[c.cli] = conn
        self.sel.register(conn, selectors.EVENT_READ, self.read)

    def run(self):
        sock = socket.socket()
        sock.bind(self.server_addr)
        sock.listen(1024)
        sock.setblocking(False)
        self.sel.register(sock, selectors.EVENT_READ, self.accept)
        while True:
            events = self.sel.select()
            for key, mask in events:
                callback = key.data
                callback(key.fileobj, mask)


parser = argparse.ArgumentParser()
parser.add_argument('-c', '--client', action='store', required=True, help='target machine ip')
parser.add_argument('-s', '--server', action='store', required=True, help='server machine ip or proxy server ip')
args = parser.parse_args()
c_host, c_port = args.client.split(':')
s_host, s_port = args.server.split(':')

s = Server(s_host, int(s_port), c_host, int(c_port))
s.start()
s.join()
