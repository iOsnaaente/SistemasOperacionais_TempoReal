import socket

HOST = ''              # Endereco IP do Servidor
PORT = 5000            # Porta que o Servidor esta

# Criação do socket no protocolo SOCK_DGRAM = UDP 
udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Definição do ADDR do servidor 
orig = (HOST, PORT)

# Início do Servidor, começa a escutar no endereço orig
udp.bind(orig)

while True:
	
    # Recebe mensagem e addr com a função refvfrom(BUFF_SIZE)
    msg, cliente = udp.recvfrom(1024)

    print (cliente, msg)

# Encerra o socket 
udp.close()



