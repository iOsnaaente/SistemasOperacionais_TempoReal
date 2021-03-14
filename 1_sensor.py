#!/usr/bin/env python3

from SocketsTCP.TCP_Client import Client_TCP    # Importa o módulo TCP
from Serial.Serial_SR import Serial_SR          # Importa o módulo Serial 

from threading import Thread                    # Importa as Threads
from struct import pack                         # Usado para codificar as mensagens em bytes

import time
import sys 
import os 


# MACRO-DEFINIÇÕES 
COMPORT = 'COM3'                                # Poderia ser pego como argumento args[1]
HOST    = '25.8.200.93'
PORT    = 1234

PERIOD  = 500                                   # Periodo do ciclo em ms
NAME    = b'S'                                  # Nome do serviço 

# INSTANCIAMENTO DA CLASSE CLIENTE 
print("Iniciando a conexão cliente/servidor...")
cliente = Client_TCP( HOST, PORT, timeout = 1 )

# SE O CLIENTE NÃO ESTIVER CONECTADO, TENTE CONECTAR ATÉ CONSEGUIR
tries = 0  
while not cliente.isAlive:
    time.sleep(1)
    cliente.connect_server() 
    tries += 1 
    if tries > 5:
        print("Servidor indisponível, encerrando processo")
        # ENCERRA COM ERRO 
        sys.exit(1)                      
print("Conexão cliente/servidor estabelecida...")


# INSTANCIAMENTO DA CLASSE SERIAL READER 
print("Iniciando a conexão Serial na comport %s ..." %( COMPORT if COMPORT else 'defalt') )
comport = Serial_SR( COMPORT )


# CONEXÕES EFETUADAS COM SUCESSO, SEGUIMOS PARA O CÓDIGO
print("Conexões Serial estabelecida....")
input("Pressione ENTER para iniciar a transmissão....")
os.system( 'clear' if os.name == 'nt' else 'cls' )       # Limpa a tela do prompt


var_global_control = True    # Avisa o fim do código 
to_send            = 0       # Variavel global dos dados 

# FUNÇÕES DE THREADS PARA LER SERIAL PERIODICO E ENVIAR DADOS
def read_serial( time_to_read = 1 ):
    global var_global_control
    global to_send 

    while var_global_control: 
        time.sleep( time_to_read )
        lines = comport.serial_receive()     
        for line in  lines:           
            data = line.decode()
            data = data.replace('\n', '').replace('\r','')
            #to_send = pack('cf', NAME, data )
            to_send = data.encode() 


def send_to_server( time_to_send = 1/2 ):
    global var_global_control
    global to_send

    while var_global_control: 
        time.sleep( time_to_send )
        cliente.send_message( to_send )


# INSTANCIA AS THREADS PASSANDO A FUNÇÃO, PARAMETROS E NOME (IDs)
func_reader = Thread( target = read_serial, args = ( 1/2 , ), name = "Serial_Reader"  )
func_sender = Thread( target = send_to_server, args = ( 1/2 , ), name = "TCP_sender" )

# INICIA AS THREADS FUNCTIONS 
func_reader.start()
func_sender.start()


time.sleep(3600000) # 60 minutos e encerra o programa 
var_global_control = False
print('Passados 60 minutos, o programa esta encerrando, por hoje é isso pessoal....')

# Sys.exit( zero = tudo ok e 1 = erro )
sys.exit(0)