#!/usr/bin/env python3

from SocketsTCP.TCP_Client import Client_TCP    # Importa o módulo TCP
from Serial.Serial_SR import Serial_SR          # Importa o módulo Serial 

from threading import Thread                    # Importa as Threads
from struct import pack                         # Usado para codificar as mensagens em bytes

import socket
import time
import sys 
import os 

# MACRO-DEFINIÇÕES 
COMPORT = 'COM4'                                # Poderia ser pego como argumento args[1]
HOST    = '25.59.115.113'
PORT    = 1234

# 'A' de atuador 
NAME = b'A'                                     # Nome do serviço 
 

# INSTANCIAMENTO DA CLASSE CLIENTE 
print("Iniciando a conexão cliente/servidor...")
cliente = Client_TCP( HOST, PORT, timeout = 1/2)

# SE O CLIENTE NÃO ESTIVER CONECTADO, TENTE CONECTAR ATÉ CONSEGUIR
tries = 0  
while not cliente.isAlive:
    time.sleep(1)
    cliente.connect_server() 
    tries += 1
    if tries > 5:
        print("Servidor indisponível, encerrando processo")
        sys.exit(1)                      # ENCERRA COM ERRO

# INSTANCIAMENTO DA CLASSE SERIAL READER 
print("Iniciando a conexão Serial na comport %s ..." %( COMPORT if COMPORT else 'default') )
comport = Serial_SR(COMPORT,timeout=1/10)

# CONEXÕES EFETUADAS COM SUCESSO, SEGUIMOS PARA O CÓDIGO
input("Conexões estabelecidas.... Pressione ENTER para iniciar a transmissão....")
# LIMPA A TELA 
#os.system( 'clear' if os.name == 'nt' else 'cls' )



serial_msg         = b'0'       # Variavel global
var_available      = False    # Mutex improvisado
var_global_control = True    # Avisa o fim do código
LIST = []

def receive_from_server(time_wait = 1/2):
    global var_global_control
    global var_available
    global serial_msg

    while var_global_control:
        #time.sleep(time_to_send)
        cliente.send_message( NAME )                           # Envia 'A'
        serial_msg = cliente.receive_message( False )           # Recebe a resposta

        # Recebe uma tupla 
        # ( b'sem dados', (0, b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00') )  
        # 0 é os dados e 1 é a conexão 
        
        try:

            serial_msg = serial_msg[0]
            print(int.from_bytes(serial_msg,byteorder='little'))
            LIST.append(serial_msg)
            #print(serial_msg, type(serial_msg))
            #serial_msg = int.from_bytes(serial_msg, byteorder='little')
            var_available = True
        
        except:
            var_available = False
            print("sem dados")
        time.sleep(1/4)

        
# FUNÇÕES DE THREADS PARA LER SERIAL PERIODICO E ENVIAR DADOS
def write_serial(time_to_read = 1/2):
    
    global var_global_control
    global var_available
    global serial_msg

    while var_global_control:
        if var_available:
            while LIST:

                #serial_msg = int.to_bytes(serial_msg, 4, byteorder='little')
                print(LIST)
                serial_msg2 = LIST.pop(0) + b'\n'
                # Envia a mensagem
                comport.serial_send( serial_msg2 )
                # Recebo uma resposta
                recebido = comport.serial_receive()

                print("Enviando para o Arduino : ", serial_msg2 )
                print("Recebendo do arduino : ", recebido )

            var_available = False 


# Limpa o buffer para enviar os dado para a serial    
comport.serial_clear_input()  
comport.serial_clear_output() 

# INSTANCIA AS THREADS PASSANDO A FUNÇÃO, PARAMETROS E NOME (IDs)
func_writer   = Thread(target = receive_from_server, args = ( 1/2 , ), name = "TCP_Reader")
func_receiver = Thread(target = write_serial, args = ( 1/2 , ), name = "Serial_Writer")

# INICIA AS THREADS FUNCTIONS 
func_receiver.start()
func_writer.start()


time.sleep(3600000) # 60 minutos e encerra o programa 
var_global_control = False
print('Passados 60 minutos, o programa esta encerrando, por hoje é isso pessoal....')

# Sys.exit( zero = tudo ok e 1 = erro )
sys.exit(0)