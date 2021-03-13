from socket import *

host = gethostname()                    # endereço do host
port = 555                              # porta p/coneção

client = socket ( AF_INET, SOCK_STREAM )
client.connect( (host, port) )
esp = "S "
while True:
    msg = ""
    msg = input("Digite:")
    msg = esp + msg
    client.send(msg.encode())          # envia mensagem p/servidor
    #response = client.recv(4096)       # resposta que o servidor fornece
    #resposta = response.decode("utf-8")
    #print(resposta)