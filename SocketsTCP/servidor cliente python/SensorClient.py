from socket import *

#host = "25.114.157.253"                 #http://25.94.218.230:555                    # endereço do host
host = gethostname()
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