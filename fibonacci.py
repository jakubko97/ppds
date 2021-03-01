from time import sleep
from random import randint
from fei.ppds import Thread, Mutex, Semaphore, print, Event

class Fibonacci():
    def __init__(self, shared, N):
        self.N = N
        self.counter = 0
        self.shared = shared
        self.mutex = Mutex()
        self.e = Event()

    def wait(self):
        if self.shared.i+2 == self.shared.end:
            self.e.wait()
            return
        self.shared.mutex.lock()
        self.counter+=1
        if self.counter == self.N:
           self.counter = 0
           for _ in range(self.N):
               self.e.signal()

        self.shared.array.append(self.shared.array[self.shared.i] + self.shared.array[self.shared.i+1])
        # print('%d ' % self.shared.array[self.shared.i])
        self.shared.i+=1
        self.shared.mutex.unlock()
        self.e.wait()

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

thread_num = 2
shared = Shared(10)
barrier = Fibonacci(shared, thread_num)
for i in range(thread_num):
    thread = Thread(barrier_example, barrier, i)

for j in shared.array:
    print('%d ' % j)

