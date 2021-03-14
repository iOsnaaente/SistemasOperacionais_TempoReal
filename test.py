from Serial.Serial_SR import Serial_SR          # Importa o módulo Serial 
from struct import pack, unpack

# MACRO-DEFINIÇÕES 
COMPORT = 'COM3'                                # Poderia ser pego como argumento args[1]
NAME = b'S'

# INSTANCIAMENTO DA CLASSE SERIAL READER 
print("Iniciando a conexão Serial na comport %s ..." %( COMPORT if COMPORT else 'defalt') )
comport = Serial_SR( COMPORT )

import time 

time.sleep(2)

lines = comport.serial_receive()     
for line in  lines:           
    data = line.decode()
    data = data.replace('\n', '').replace('\r','').encode()
    to_send = pack('cf', NAME, 3.14157 )
    print(type(to_send), to_send )
    caracter, valor = unpack('cf', to_send)
    print( caracter, valor )