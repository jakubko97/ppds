from time import sleep
from random import randint
from fei.ppds import Thread, Mutex, Semaphore, print

class SimpleBarrier():
    def __init__(self, N):
        self.N = N
        self.counter = 0
        self.mutex = Mutex()
        self.turnstile = Semaphore(0)

    def wait(self, shared):
        if self.counter == self.N:
            for _ in range(self.N):
                self.turnstile.signal()
                return

        self.mutex.lock()
        self.counter+=1
        shared.array.append(shared.array[shared.i] + shared.array[shared.i+1])
        print('i : {%d} ' % shared.array[shared.i])
        shared.i+=1
        self.mutex.unlock()
        self.turnstile.wait()

class Shared():
    def __init__(self, end):
        self.i = 0
        self.end = end
        self.array = []
        self.array.append(0)
        self.array.append(1)
        self.mutex = Mutex()

def rendezvous(thread_name):
    sleep(randint(1,10)/10)
    print('vlakno: {%d} pred barierou' % thread_name)

def ko(thread_name):
    print('vlakno: {%d} po bariere' % thread_name)
    sleep(randint(1,10)/10)


def barrier_example(barrier, shared, thread_name):

    for _ in range(shared.end):
        # ...
        rendezvous(thread_name)
        barrier.wait(shared)
        ko(thread_name)
        # ...

thread_num = 8
barrier = SimpleBarrier(thread_num)

sh = Shared(10)
for i in range(thread_num):
    thread = Thread(barrier_example, barrier, sh, i)

