from socket import *

host = gethostname()                    # endereço do host
port = 555                              # porta p/coneção

client = socket ( AF_INET, SOCK_STREAM )
client.connect( (host, port) )
#esp = "A "
msg = "A Esperando ação"
while True:
    #print(client)
    #msg = input("Digite:")
    #msg = esp + msg
    client.send(msg.encode())          # envia mensagem p/servidor
    response = client.recv(4096)         # resposta que o servidor fornece
    resposta = response.decode("utf-8")
    if resposta != "sem dados":
        print(resposta)