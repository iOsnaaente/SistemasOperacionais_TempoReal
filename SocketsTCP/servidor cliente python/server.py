from socket import *
import socketserver, time

import Threads2
import threading

host = gethostname()
port = 555

def agora():
    return time.ctime( time.time() )

class LidarcomCliente( socketserver.BaseRequestHandler ):                                                # Classe para lidar com a conexao dos clientes

    def handle(self):
        print(self.client_address, agora() )
        def situacao(strinfodata):
            if strinfodata[0:1] == "A":
                return "Atuador"
            elif strinfodata[0:1] == "S":
                return "Sensor"
        while True:                                                                                       # Laço de execução do Servidor
            infodata = self.request.recv(1024)                                                            # informação que recebeu do cliente
            strinfodata = infodata.decode("utf-8")
            print( self.client_address, strinfodata )                                                     # Qual cliente enviou a mensagem e a mensagem
            if not infodata:
                break
            resposta = '%s, msg: %s, DataHora %s' % (situacao(strinfodata),strinfodata, agora())          # cria uma resposta p/ enviar
            self.request.send(resposta.encode())                                                          # envia p/ cliente uma resposta qualquer
        
        self.request.close()

ender = (host,port)
server = socketserver.ThreadingTCPServer( ender, LidarcomCliente)                                         # Cria servidor
server.serve_forever()                                                                                    # P/ sempre executar
