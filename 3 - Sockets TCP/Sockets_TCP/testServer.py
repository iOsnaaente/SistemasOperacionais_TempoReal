from TCP_Server import Server_TCP 

sr = Server_TCP( 'localhost', 1205, 10)

sr.start()

clientes = sr.get_clients_connected()

sr.receive_message( clientes[-1][0], True )




sr.connection = False 