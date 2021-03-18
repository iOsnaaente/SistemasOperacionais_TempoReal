import socket
import struct
import time 
import sys 

HOST = '25.86.62.64'  # Endereco IP do Servidor
PORT = 5000        # Porta que o Servidor esta

# Criação do socket no protocolo SOCK_DGRAM = UDP 
udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Definição do ADDR do servidor 
dest = (HOST, PORT)

# Variável da mensagem a ser transmitida 
i = str("TE AMO MINHA LINDA!!")
a = str(time.time())

while True:

    i = str("TE AMO MINHA LINDA!!")
    a = str(time.time())

    msg = i + a
    msg = msg.encode()
    
    print( type(i), sys.getsizeof(i), i)
    msg = str(i).encode()


    # Envia a mensagem para o endereço do servidor
    udp.sendto (msg, dest)

# Encerra o Socket
udp.close()


