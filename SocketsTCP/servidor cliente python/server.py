from socket import *
import socketserver, time
from threading import Thread

import Threads2
import threading

host = "25.114.157.253"
port = 555
LIST = []
msg1 = "sem dados"

class Thatuador(Thread):
    def __init__(self, info):
        Thread.__init__(self)
        self.info = info


    def run(self):

        while LIST:
            msg = ""
            for msg in LIST:
                #print(LIST)
                self.info.request.send(msg.encode())
                #info.remove(msg)
                LIST.remove(msg)
        #print("nao entrou")
        self.info.request.send(msg1.encode())
class Thsensor(Thread):
    def __init__(self, info):
        Thread.__init__(self)
        self.info = info

    def run(self):
        LIST.append(self.info)
        #print(LIST)

def agora():
    return time.ctime( time.time() )


def situacao(self,strinfodata):
    if strinfodata[0:1] == "A":
        atuador = self
        th = Thatuador(atuador)
        th.start()
    elif strinfodata[0:1] == "S":
        th = Thsensor(strinfodata)
        th.start()

class LidarcomCliente( socketserver.BaseRequestHandler ):                                                # Classe para lidar com a conexao dos clientes
    #print(host)
    def handle(self):
        while True:                                                                                       # Laço de execução do Servidor
            infodata = self.request.recv(1024)                                                            # informação que recebeu do cliente
            strinfodata = infodata.decode("utf-8")
            if not infodata:
                break
            situacao(self,strinfodata)

        self.request.close()

ender = (host,port)
server = socketserver.ThreadingTCPServer(ender, LidarcomCliente)                                         # Cria servidor
server.serve_forever()                                                                                    # P/ sempre executar
