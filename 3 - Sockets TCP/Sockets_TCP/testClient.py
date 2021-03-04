from TCP_Client import Client_TCP 

cl = Client_TCP( 'localhost', 1205, 1)

cl.send_message( 'Hello World !! ' )

#cl.receive_message( True )

