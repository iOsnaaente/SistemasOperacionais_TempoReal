from socket import *
import socketserver, time
from threading import Thread

import Threads2
import threading

host = gethostname()
port = 555
LIST = []

class Thatuador(Thread):
    def __init__(self, info):
        Thread.__init__(self)
        self.info = info


    def run(self):
        while LIST:
            for msg in LIST:
                #print(LIST)
                self.info.request.send(msg.encode()) # dando merda nesse self deve ser passado o socket
                #info.remove(msg)
                LIST.remove(msg)
        #print("nao entrou")
        msg = "sem dados"
        self.info.request.send(msg.encode())
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
        #print("atuador")
        #print("type",type(self))
        #print(atuador)
        th = Thatuador(atuador)
        th.start()
        #self.request.send(strinfodata.encode())   #aqui deu bom +-
    elif strinfodata[0:1] == "S":
        th = Thsensor(strinfodata)
        th.start()
        #print("sensor")

class LidarcomCliente( socketserver.BaseRequestHandler ):                                                # Classe para lidar com a conexao dos clientes

    def handle(self):
        #print(self.client_address, agora() )
        #print(self)
        while True:                                                                                       # Laço de execução do Servidor
            infodata = self.request.recv(1024)                                                            # informação que recebeu do cliente
            strinfodata = infodata.decode("utf-8")
            #print( self.client_address, strinfodata )                                                     # Qual cliente enviou a mensagem e a mensagem
            if not infodata:
                break
            #resposta = 'msg: %s, DataHora %s' % (strinfodata, agora())          # cria uma resposta p/ enviar
            #self.request.send(resposta.encode())                                                          # envia p/ cliente uma resposta qualquer
            situacao(self,strinfodata)

        self.request.close()

ender = (host,port)
server = socketserver.ThreadingTCPServer( ender, LidarcomCliente)                                         # Cria servidor
server.serve_forever()                                                                                    # P/ sempre executar
