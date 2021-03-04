from serial import Serial, SerialException
from sys import platform
from glob import glob

"""
    A classe funciona tanto em Windows quanto em Linux 
    
    Testa todas as portas possíveis no computador e tenta abri-las
        Caso ele consiga, significa que a porta existe
        Caso a porta não possa ser aberta, ela existe
        Caso retorne Erro (SerialException), ela não existe
    
    Retorna uma lista com os nomes das portas disponíveis 

    Bruno Gabriel Flores Sampaio

"""

class Serial_SR ( Serial ):
    
    comport = 0 
    baudrate = 0 
    timeout = 0 

    def __init__(self, comport = 0, baudrate = 9600, timeout = 1):
        super().__init__(self)

        self.comport  = comport 
        self.baudrate = baudrate
        self.timeout  = timeout

        if not comport:
            comports = self.get_SerialPorts()
            for comport_ in comports:
                self.comport = comport_
                print("Tentando conectar na Comport : ", comport_ )
                try: 
                    self.init_SerialPort(comport_, self.baudrate, self.timeout)
                    print("Comport : ", comport_ , " conectada!!")
                    break
                except:
                    pass
            if not self.comport:
                print("Não foram encontradas Portas seriais válidas, verifique a conexão e tente novamente")
        else:
            try:
                self.init_SerialPort( self.comport, self.baudrate, self.timeout )
            except:
                print("Não foi possível conectar na comport : ", self.comport )


    """ Seta a porta serial conectada 
    """
    def set_port(self, comport):
        try:
            self.init_SerialPort(comport, self.baudrate, self.timeout)
            try: 
                self.close()
            except:
                pass
            self.comport = comport
        except:
            print("Não foi possível conectar na comport : ", self.comport )
            print("Ainda conectado em : ", self.comport )
    

    """ Retorna uma lista de portas seriais disponíveis
    """
    def get_SerialPorts(self, limit = 10 ):

        # Abre se o SO for Windows
        if platform.startswith('win'):  
            ports = ['COM%s' % (i + 1) for i in range( limit )]
        
        # Abre se o SO for Linux
        elif platform.startswith('linux') or platform.startswith('cygwin'):
            ports = glob('/dev/tty[A-Za-z]*')
        
        # Caso não seja nenhum dos dois, ele não suporta
        else:
            print("Sistema Operacional não suportado")

        # Testa as portas disponíveis 
        portList = []
        for port in ports:
            try:
                s = Serial(port)
                s.close()
                portList.append(port)
            except (OSError, SerialException):
                pass

        return portList


    """ Mostra a lista de portas seriais disponíveis
    """
    def show_SerialPorts(self):
        listaPortas = self.get_SerialPorts()
        if listaPortas is None:
            print("Não há portas Seriais abertas !!")
        else:
            for port in listaPortas:
                print(port, end="\n")


    """ Inicia a conexão serial 
    """
    def init_SerialPort(self, DEVICE = self.comport, BAUDRATE = self.baudrate, TIMEOUT = self.timeout):
        # Inicia a conexao serial
        #comport = serial.Serial('/dev/ttyUSB4', 9600, timeout=1)
        self.comport = Serial(DEVICE, BAUDRATE, TIMEOUT)
        return comport
    
    
    """ Retorna a leitura da porta serial
    """
    def serial_receive(self ):
        return self.comport.read()


    """ Envia uma mensagem literal para a porta serial
    """
    def serial_send(self, msg):
        self.comport.write( msg )


    """ Seta o baudarate da porta conectada.
        A função reset_comport() deve ser chamada para reiniciar a conexão 
    """
    def set_baudrate(self, baudrate):
        self.baudrate = baudrate


    """ Seta o timeout da porta conectada.
        A função reset_comport() deve ser chamada para reiniciar a conexão
    """
    def set_timeout(self, timeout):
        self.timeout = timeout


    """ Finaliza a conexão atual e inicia com as novas configurações
    """
    def reset_comport(self):
        try:
            self.close()
        except:
            pass
        self.init_SerialPort()


    """ Encerra a conexão da porta serial
    """
    def close_SerialPort(self):
        # Fechando conexao serial
        self.comport.close()