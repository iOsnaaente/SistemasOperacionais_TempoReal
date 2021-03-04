import socket

class Client_TCP:

    HOST    = '127.0.0.1'     # IP address 
    PORT    = 5000            # Port where the server is connected
    TIMEOUT = 1               # Timeout in seconds 
    BUFF    = 1024            # Buffer to receive n bytes 

    
    def __init__(self, HOST, IP, timeout = 0, server = False ):

        self.HOST     = HOST
        self.IP       = IP  
        self.TIMEOUT  = timeout
        self.BUFF     = 1024

        # Cria o socket TCP 
        self.tcp = socket.socket( socket.AF_INET, socket.SOCK_STREAM )

        # Seta o Timeout para bloqueante ou não bloqueante 
        if self.TIMEOUT:
            self.tcp.settimeout( self.TIMEOUT )

        # Cria a tupla addr do server 
        self.server_addr = (HOST, IP)

        # Chama o método de conexão do servidor
        self.connect_server()

    """ Para se conectar em um servidor                                                  
    """
    def connect_server ( self ):
        try: 
            # Conecta no servidor no host e ip passados
            self.tcp.connect( self.server_addr )
        except:
            print("Falha para conectar no servidor : ", self.server_addr ) 


    """ Para mandar uma mensagem TCP usar o método abaixo.
        Padrão usar mensagens str.encode() ou str. 
    """
    def send_message( self, msg ):
        # Garante que a mensagem esteja codificada
        if type(msg) is str:
            msg = msg.encode()
        elif type(msg) is not bytes:
            print("Dados fora do padrão de envio TCP != str or bytes")

        self.tcp.send( msg )


    """ Método para receber uma mensagem.
        Lembrar do timeout (segundos).
    """
    def receive_message(self ):
        msg = self.tcp.recvfrom( self.BUFF ) 
                

    """ setar o tamanho máximo do buffer.
    """
    def set_buffer(self, buff):
        self.BUFF = buff 


    """
        Setar o timeout da conexão.
    """
    def set_timeout(self, timeout):
        self.TIMEOUT = timeout
        self.tcp.settimeout( self.TIMEOUT )


    """ Encerrar a conexão TCP.
    """
    def close_connection(self):
        self.tcp.close()



