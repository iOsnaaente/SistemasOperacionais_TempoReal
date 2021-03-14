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
COMPORT = 'COM3'                                # Poderia ser pego como argumento args[1]
HOST    = '25.114.157.253'      
PORT    = 1234

# 'A' de atuador 
NAME = b'A'                                     # Nome do serviço 
 

# INSTANCIAMENTO DA CLASSE CLIENTE 
print("Iniciando a conexão cliente/servidor...")
cliente = Client_TCP( HOST, PORT, timeout = 5)

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
comport = Serial_SR(COMPORT)

# CONEXÕES EFETUADAS COM SUCESSO, SEGUIMOS PARA O CÓDIGO
input("Conexões estabelecidas.... Pressione ENTER para iniciar a transmissão....")
# LIMPA A TELA 
#os.system( 'clear' if os.name == 'nt' else 'cls' )



serial_msg         = 0       # Variavel global
var_available      = True    # Mutex improvisado
var_global_control = True    # Avisa o fim do código

def receive_from_server(time_to_send = 1/2):
    global var_global_control
    global var_available
    global serial_msg

    while var_global_control:
        #time.sleep(time_to_send)
        cliente.send_message( NAME )                           # Envia 'A'
        serial_msg = cliente.receive_message( True )           # Recebe a resposta
        var_available = True 


# FUNÇÕES DE THREADS PARA LER SERIAL PERIODICO E ENVIAR DADOS
def write_serial(time_to_read = 1/2):
    
    global var_global_control
    global var_available
    global serial_msg

    while var_global_control:
        if var_available:

            if type(serial_msg) is not None: 
                if type(serial_msg) is not bytes: 
                    serial_msg.encode()
                     
                comport.serial_send( serial_msg )
                var_available = False 
    

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