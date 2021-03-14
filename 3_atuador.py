from TCP_Client import Client_TCP
from Serial_SR import Serial_SR

from threading import Thread

import time 
import sys 
import os

# MACRO-DEFINIÇÕES 
COMPORT = 0
HOST    = gethostname()
PORT    = 1205

PERIOD = 500                                    # Periodo do ciclo 
NAME = b'A'                              # Nome do serviço 

TERMINAL_SIZE = os.get_terminal_size().lines    # "Limpar" a tela com '\n' 

# INSTANCIAMENTO DA CLASSE CLIENTE 
print("Iniciando a conexão cliente/servidor...")
cliente = Client_TCP( HOST, PORT, timeout = 1)

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
cliente.send_message(NAME.encode())

# INSTANCIAMENTO DA CLASSE SERIAL READER 
print("Iniciando a conexão Serial na comport %s ..." %( COMPORT if COMPORT else 'default') )
comport = Serial_SR(COMPORT)

# CONEXÕES EFETUADAS COM SUCESSO, SEGUIMOS PARA O CÓDIGO
input("Conexões estabelecidas.... Pressione ENTER para iniciar a transmissão....")
print('\n' * TERMINAL_SIZE) # SAME AS os.system( 'clear' if os.name == 'nt' else 'cls' )


to_send            = 0       # Variavel global
var_available      = True    # Mutex improvisado
var_global_control = True    # Avisa o fim do código

def receive_from_server(time_to_send = 1/2):
    
    global var_global_control
    global var_available
    global serial_msg

    while var_global_control:
        time.sleep(time_to_send)
        cliente.send_message(NAME)
        serial_msg = cliente.receive_message().decode()
        
# FUNÇÕES DE THREADS PARA LER SERIAL PERIODICO E ENVIAR DADOS
def write_serial(time_to_read = 1/2):
    
    global var_global_control
    global var_available
    global serial_msg

    while var_global_control:
        comport.serial_send(serial_msg)
    
# INSTANCIA AS THREADS PASSANDO A FUNÇÃO, PARAMETROS E NOME (IDs)
func_reader = Thread(target = receive_from_server, args = ( 1/2 , ), name = "TCP_Reader")
func_sender = Thread(target = write_serial, args = ( 1/2 , ), name = "Serial_Writer")

# INICIA AS THREADS FUNCTIONS 
func_reader.start()
func_sender.start()

# RODA AS FUNÇÕES ATÉ RECEBER UM CARACTER ESPECIAL 
while True:
    func = int(input('Pressione 0 (zero) para encerrar o código')) 
    if func == 1:
        debug = not debug 
    elif func == 0:
        var_global_control = False
        break
    else:
        continue 