from time import sleep
from random import randint
from fei.ppds import Thread, Mutex, Semaphore, print

# Vypisovat na monitor budeme pri zamknutom mutexe pomocou
# funkcie 'print' z modulu 'fei.ppds', aby sme nemali rozbite vypisy.

from fei.ppds import print

class SimpleBarrier():
    def __init__(self, N):
        self.N = N
        self.counter = 0
        self.mutex = Mutex()
        self.turnstile1 = Semaphore(0)
        self.turnstile2 = Semaphore(0)

    def wait(self):
        self.mutex.lock()
        self.counter +=1
        if self.counter == self.N:
           self.counter = 0
           for _ in range(self.N):
               self.turnstile1.signal()
        self.mutex.unlock()
        self.turnstile1.wait()

        # self.mutex.lock()
        # self.counter -= 1
        # if self.counter == 0:
        #    self.turnstile2.signal()
        #    self.turnstile1.wait()
        # self.mutex.unlock()
        # self.turnstile2.wait()
        # self.turnstile1.signal()

class Barrier:
     def __init__(self, N):
        self.sb1 = SimpleBarrier(N)
        self.sb2 = SimpleBarrier(N)

     def wait(self):
        self.sb1.wait()
        self.sb2.wait()

def rendezvous(thread_name):
    sleep(randint(1,10)/10)
    print('vlakno: {%d} pred barierou' % thread_name)

def ko(thread_name):
    print('vlakno: {%d} po bariere' % thread_name)
    sleep(randint(1,10)/10)


def barrier_example(barrier,thread_name):
    # Kazde vlakno vykonava kod funkcie 'barrier_example'.
    # Doplnte synchronizaciu tak, aby sa vsetky vlakna pockali
    # nielen pred vykonanim funkcie 'ko', ale aj
    # *vzdy* pred zacatim vykonavania funkcie 'rendezvous'.

    while True:
        # ...
        rendezvous(thread_name)
        barrier.wait()
        ko(thread_name)
        # ...


# Vytvorime vlakna, ktore chceme synchronizovat.
# Nezabudnime vytvorit aj zdielane synchronizacne objekty,
# a dat ich ako argumenty kazdemu vlaknu, ktore chceme pomocou nich
# synchronizovat.

thread_num = 5
sb1 = SimpleBarrier(thread_num)
sb2 = SimpleBarrier(thread_num)
barrier = Barrier(thread_num)
for i in range(thread_num):
    thread = Thread(barrier_example, barrier, i)
