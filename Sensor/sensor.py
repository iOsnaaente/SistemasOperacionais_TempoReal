from TCP_Client import Client_TCP
from Serial_SR import Serial_SR

from threading import Thread

import time 
import sys 
import os 

# MACRO-DEFINIÇÕES 
COMPORT = 'COM5'
HOST    = 'localhost'
PORT    = 1205

PERIOD = 500                                    # Periodo do ciclo 
NAME = 'Sensor'.encode()                        # Nome do serviço 

TERMINAL_SIZE = os.get_terminal_size().lines    # "Limpar" a tela com '\n' 


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
        sys.exit(1)                      # ENCERRA COM ERRO 

# AVISA O SERVIDOR QUEM É 
cliente.send_message( NAME )


# INSTANCIAMENTO DA CLASSE SERIAL READER 
print("Iniciando a conexão Serial na comport %s ..." %( COMPORT if COMPORT else 'defalt') )
comport = Serial_SR( COMPORT )


# CONEXÕES EFETUADAS COM SUCESSO, SEGUIMOS PARA O CÓDIGO
input("Conexões estabelecidas.... Pressione ENTER para iniciar a transmissão....")
print( '\n' * TERMINAL_SIZE ) # SAME AS os.system( 'clear' if os.name == 'nt' else 'cls' )


to_send            = 0       # Variavel global
var_available      = True    # Mutex improvisado
var_global_control = True    # Avisa o fim do código 

# FUNÇÕES DE THREADS PARA LER SERIAL PERIODICO E ENVIAR DADOS
def read_serial( time_to_read = 1 ):
    global var_global_control
    global var_available
    global to_send 

    while var_global_control: 
        time.sleep( time_to_read )
        lines = comport.serial_receive()     
        for line in  lines:
            var_available = False            
            to_send = line.decode()         
            print( to_send )
            var_available = True 

def send_to_server( time_to_send = 1 ):
    global var_global_control
    global var_available
    global to_send

    while var_global_control: 
        time.sleep( time_to_send )
        cliente.send_message( var_available )


# INSTANCIA AS THREADS PASSANDO A FUNÇÃO, PARAMETROS E NOME (IDs)
func_reader = Thread( target = read_serial, args = 1/2, name = "Serial_Reader"  )
func_sender = Thread( target = send_to_server, args = 1/2, name = "TCP_sender" )

# INICIA AS THREADS FUNCTIONS 
func_reader.start()
func_sender.start()

# RODA AS FUNÇÕES ATÉ RECEBER UM CARACTER ESPECIAL 
while True:
    func = int( input('Pressione 0 (zero) para encerrar o código') ) 
    if func == 1 :
        debug = not debug 
    elif func == 0:
        var_global_control = False
        break
    else:
        continue 