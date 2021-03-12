from threading import Thread, Lock
from sys import stdout
from time import time 

class Parallel_task ( Thread ):

    def __init__(self, id, func, *args, **kwargs):
        Thread.__init__(self)

        self.mutex  = Lock()
        self.func   = func
        self.id     = id 

        self.args   = *args 
        self.kwargs = **kwargs


    # Execução do método Start() da Thread 
    def run (self):

        # Chama a execução da Função passada
        # Aplica a função enviada como argumento, junto com os 
        # argumentos e keywords argumentos
        self.result = self.f(self.args, self.kwargs) 
        try:
            # Try to unpack
            self.result = *self.result
        except:
            # Else alread unpacked 
            pass 

        # Importante para não acessar arquivos compartilhados
        with self.mutex:
            stdout.write("Finalizados os ciclos da thread" )  