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

from struct import pack, unpack 


lines = comport.serial_receive() 

for line in  lines:   

    data = str( line.decode() ).split(' ')
    data = data[:-1]
    data = [ int(n) for n in data ]
    print(data)
    
    valor = bytes(data)

    teste = int.from_bytes( valor, byteorder='little')




    print(teste)