from threading import Thread, Lock
from sys import stdout
from time import time 

class Parallel_task ( Thread ):

    def __init__(self, id, func):
        Thread.__init__(self)

        self.mutex  = Lock()      # Usa um Mutex para sinalizar uso 
        self.func   = func        # Função que será passada para uso em thread
        self.id     = id          # Identificação por nome, numero ou tag 

    # Execução do método Start() da Thread 
    def run (self):
        self.func()