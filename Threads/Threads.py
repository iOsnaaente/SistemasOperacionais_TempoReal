from threading import Thread, Lock

import time 
import sys

class Trehdis ( Thread ):

    def __init__(self, id, func,  rep = 1 ):
        Thread.__init__(self)

        self.mutex  = Lock()
        self.rep    = rep
        self.id     = id 
        self.f      = func

    def run (self):
        num_cycles  = self.rep
        num = 0

        self.time_begin = time.time()
        for i in range(num_cycles):
            with self.mutex:
                result = self.f( num )
                sys.stdout.write( "Thread %s : %d \n" %( self.id, result ) )
                num += 1
        self.time_finished = time.time()

        self.time_accumulated = (self.time_finished - self.time_begin)

        # Importante para não acessar arquivos compartilhados
        with self.mutex:
            sys.stdout.write("Finalizados os ciclos da thread: %s -> Tempo %2.5f \n" %(self.id, self.time_accumulated) )  


# Criamos a função que será usada na Thread 
def dobro ( num ):
    return 2*num


# Numero de threads que serão usadas 
NUM_THREADS = 500

# Função main para teste
if __name__ == "__main__":

    threads = [] 
    for i in range(NUM_THREADS):
        t = Trehdis("["+str(i)+"]", dobro, 10  )
        t.start()
        threads.append(t)
    
    media = 0
    val = [] 
    for t in threads:
        t.join()
        val.append(t.time_accumulated)
    
    media = sum(val)/NUM_THREADS

    print("Jitter médio das threads = " + str(media)  )