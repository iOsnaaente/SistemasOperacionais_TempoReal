from threading import Thread
from socket import *

import socketserver, time
import threading


from math import sqrt

host = "25.94.9.254"  # http://25.94.218.230:555
port = 1234
LIST = []

aux = 0


class Thatuador(Thread):
    def _init_(self, info):
        Thread._init_(self)
        self.info = info

    def run(self):
        if LIST:
            enviando = LIST.pop(0)
            print(enviando)
            self.info.request.send(enviando)
        else:
            # print("nao entrou")
            msg = ""
            self.info.request.send(msg.encode())


class Thsensor(Thread):
    def _init_(self, info):
        Thread._init_(self)
        self.info = info

    def run(self):
        if len(LIST) == 10:
            LIST.pop(0)

        LIST.append(self.info)
        print(LIST)


def agora():
    return time.ctime(time.time())


def situacao(self, strinfodata):
    str_val = strinfodata[:1].decode().upper()

    int_val = int.from_bytes(strinfodata[1:], byteorder='little', signed=False)

    global aux

    # PUXANDO A RAIZ DO NUMERO
    int_val = round(sqrt(int_val))
    int_val = int(int_val)

    try:
        int_val = int.to_bytes(int_val, 4, byteorder='little')
        aux = int_val
    except:
        int_val = aux

    print('int_val ', int_val)

    if str_val == "A":
        print("TH_Atuador", int_val)
        atuador = self
        th = Thatuador(atuador)
        th.start()

    elif str_val == "S":
        print("TH_Sensor", int_val)
        th = Thsensor(int_val)
        th.start()


# Classe para lidar com a conexao dos clientes
class LidarcomCliente(socketserver.BaseRequestHandler):

    def handle(self):
        while True:  # Laço de execução do Servidor
            infodata = self.request.recv(1024)  # informação que recebeu do cliente
            print('infodata ', infodata)
            if not infodata:
                break
            situacao(self, infodata)

        self.request.close()


ender = (host, port)
server = socketserver.ThreadingTCPServer(ender, LidarcomCliente)  # Cria servidor
server.serve_forever()