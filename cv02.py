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
           self.turnstile1.signal()
        self.mutex.unlock()
        self.turnstile1.wait()
        self.turnstile2.signal()

        self.mutex.lock()
        self.counter -= 1
        if self.counter == 0:
           self.turnstile2.signal()
           self.turnstile1.wait()
        self.mutex.unlock()
        self.turnstile2.wait()
        self.turnstile1.signal()


def rendezvous(thread_name, i):
    sleep(randint(1,10)/10)
    print('vlakno: {%d} pred barierou' % thread_name)

def ko(thread_name, i):
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
sb = SimpleBarrier(thread_num)
for i in range(thread_num):
    thread = Thread(barrier_example, sb, i)
