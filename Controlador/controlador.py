from TCP_Server import Server_TCP 
from Serial_SR import Serial_SR

from threading import Thread

from math import pow 

import time 
import sys 
import os 

# MACRO-DEFINIÇÕES 
HOST    = 'localhost'
PORT    = 1205

PERIOD = 500                                  # Periodo do ciclo 
NAME = 'Controlador'.encode()                 # Nome do serviço 

TERMINAL_SIZE = os.get_terminal_size().lines  # "Limpar" a tela com '\n' 

# ENCERRAR A POHA TODA 
var_exit = False

# INSTANCIAMENTO DA CLASSE SERVER 
print("Iniciando a conexão do servidor...")
server = Server_TCP( HOST, PORT, timeout = 1, num_listening = 2 )

# ENDEREÇO DOS CLIENTES 
actuator_client = 0 
sensor_client   = 0 

# LISTA DE CLIENTES QUE CONECTARAM
def new_connections( server ):
    
    global actuator_client
    global sensor_client 
    global var_exit   

    while not var_exit:
        # ESPERA RECEBER UMA CONEXÃO NO SERVIDOR
        new_client = server.connect_client()
        if new_client:
            conn, addr = new_client 
            msg = conn.recvfrom( server.BUFF )

            if msg[0].decode() == 'Sensor':
                sensor_client = new_client 
                print("Cliente conectado!!")

            elif msg[0].decode() == 'Atuador':
                actuator_client = new_client
                print("Atuador conectado!!")

            else: 
                print('Cliente conectado não identificado')


print("Iniciando escuta do servidor em busca de novas conexões...", end='\n')
server_thr = Thread( target = new_connections, args = (server,), name = "Que procura novas conexões" )
server_thr.start()


# CONEXÕES EFETUADAS COM SUCESSO, SEGUIMOS PARA O CÓDIGO
input("Conexões estabelecidas.... Pressione ENTER para iniciar a transmissão....")
print( '\n' * TERMINAL_SIZE ) # SAME AS os.system( 'clear' if os.name == 'nt' else 'cls' )


received_data = False
read_to_send  = False  

data_controll = 0 


def signal_manipulation(data):
    return pow(data, 2)


def sensor_communication(server, client, period, show_msg = False ):
    global received_data
    global var_exit
    
    while not var_exit:    
        print("Lendo os dados do sensor...")
        server.receive_message( client, show_msg = show_msg )
        received_data = True 
        time.sleep( period )


def controller_communication(data, show_msg = False ):
    global received_data
    global data_controll 
    global read_to_send 
    global var_exit

    while not var_exit:
        if received_data: 
            print("Manipulando os dados do sensor...")
            data_controll = signal_manipulation(data)
            received_data = False 
            read_to_send = True


def actuator_communication(server, client, show_msg = False ):
    global read_to_send 
    global var_exit
    
    while not var_exit:
        if read_to_send: 
            print("Enviando os dados para o atuador...")
            read_to_send = False


print('\n'*TERMINAL_SIZE)
print('Iniciando o processo')

if sensor_client:
    controller_thr = Thread( target= controller_communication, args= (data_controll, True, ), name= 'Controller')
    #actuator_thr   = Thread( target= actuator_communication, args= (server, actuator_client[0], True, ), name= 'Actuator')
    sensor_thr     = Thread( target= sensor_communication, args= (server, sensor_client[0], 5, True, ), name= 'Sensor')

    controller_thr.start()
    #actuator_thr.start()
    sensor_thr.start()

time.sleep(20)

var_exit = True