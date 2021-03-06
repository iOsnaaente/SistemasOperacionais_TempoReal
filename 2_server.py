
from threading import Thread
from socket import *

import socketserver, time
import threading

host = "25.114.157.253"  #http://25.94.218.230:555
port = 1234
LIST = []

aux = 0 

class Thatuador(Thread):
    def __init__(self, info):
        Thread.__init__(self)
        self.info = info

    def run(self):
        msg = ''
        while LIST:
            for msg in LIST:
                #print(LIST)
                self.info.request.send(msg.encode())
                #info.remove(msg)
                LIST.remove(msg)
            return 0
        #print("nao entrou")
        msg1 = ""
        msg1 = "sem dados"
        self.info.request.send(msg1.encode())
        

class Thsensor(Thread):
    def __init__(self, info):
        Thread.__init__(self)
        self.info = info

    def run(self):
        if len(LIST) == 10: 
            LIST.pop(0)
        LIST.append( self.info )
        

def agora():
    return time.ctime( time.time() )


def situacao(self, strinfodata):
    global aux 

    str_val = strinfodata[:1].decode().upper()
    
    int_val = int.from_bytes(strinfodata[1:], byteorder='little')
    print(int_val)
    
    # PUXANDO A RAIZ DO NUMERO
    int_val = int( sqrt( int_val ) ) 
    try: 
        int_val = int.to_bytes(int_val, 4, byteorder='little')
        aux = int_val 
    except:
        int_val = aux 

    if str_val == "A":
        print("Chamando TH_Atuador", int_val )
        atuador = self
        th = Thatuador( atuador )
        th.start()
    elif str_val == "S":
        print("Chamando TH_Sensor", int_val )
        th = Thsensor( int_val )
        th.start()

class LidarcomCliente( socketserver.BaseRequestHandler ):                                                # Classe para lidar com a conexao dos clientes
    
    def handle(self):
        while True:                                                                                       # Laço de execução do Servidor
            infodata = self.request.recv(1024)                                                           # informação que recebeu do cliente
            print(infodata)
            strinfodata = infodata.decode("utf-8")
            infodata = self.request.recv(1024)                                                            # informação que recebeu do cliente

            if not infodata:
                break
            situacao(self, infodata)
            

        self.request.close()

ender = (host,port)
server = socketserver.ThreadingTCPServer(ender, LidarcomCliente)                                         # Cria servidor
server.serve_forever()                                                                                    # P/ sempre executar