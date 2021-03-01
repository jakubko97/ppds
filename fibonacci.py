from time import sleep
from random import randint
from fei.ppds import Thread, Mutex, Semaphore, print

class Fibonacci():
    def __init__(self, shared, N):
        self.N = N
        self.counter = 0
        self.shared = shared
        self.turnstile = Semaphore(0)

    def wait(self):
        self.shared.mutex.lock()

        if self.shared.i+2 == self.shared.end:
            return

        self.counter+=1
        if self.counter == self.N:
           self.counter = 0
           for _ in range(self.N):
               self.turnstile.signal()

        self.shared.array.append(self.shared.array[self.shared.i] + self.shared.array[self.shared.i+1])
        # print('i : {%d} ' % self.shared.i)
        self.shared.i+=1
        self.shared.mutex.unlock()
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


def barrier_example(barrier, thread_name):
        # ...
    while True:
        # rendezvous(thread_name)
        barrier.wait()
        # ...

thread_num = 8
shared = Shared(8)
barrier = Fibonacci(shared, thread_num)
for i in range(thread_num):
    thread = Thread(barrier_example, barrier, i)

for j in shared.array:
    print('%d ' % j)

