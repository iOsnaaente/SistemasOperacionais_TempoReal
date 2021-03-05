from socket import *
import socketserver, time
import Threads2
import threading

host = gethostname()
port = 555

def agora():
    return time.ctime(time.time())

class LidarcomCliente(socketserver.BaseRequestHandler):                  # Classe para lidar com a conexao dos clientes
    def handle(self):
        print(self.client_address, agora())

        while True:                                                      # Laço de execução do Servidor
            infodata = self.request.recv(1024)                           # informação que recebeu do cliente
            print(self.client_address, infodata)                         # Qual cliente enviou a mensagem e a mensagem
            if not infodata: break
            resposta = '%s as %s' % (infodata, agora())                  # cria uma resposta p/ enviar
            self.request.send(resposta.encode())                         # envia p/ cliente uma resposta qualquer
        self.request.close()
ender = (host,port)
server = socketserver.ThreadingTCPServer(ender, LidarcomCliente)         # Cria servidor
server.serve_forever()                                                   # P/ sempre executar
