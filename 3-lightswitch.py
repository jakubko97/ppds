from time import sleep
from random import randint
from fei.ppds import Thread, Mutex, Semaphore, print, Event
# seminar ppds 2/03/2021

class LightSwitch(object):
    def __init__(self):
        self.mutex = Mutex()
        self.cnt = 0

    def lock(self, semaphore):
        # zistujeme ci sme prvy
        self.mutex.lock()
        self.cnt += 1
        if self.cnt == 1:
            semaphore.wait()
        self.mutex.unlock()

    def unlock(self, semaphore):
        # zistujeme ci sme posledny
        self.mutex.lock()
        self.cnt -= 1
        if self.cnt == 0:
            semaphore.signal()
        self.mutex.unlock()

class Shared(object):
    def __init__(self, N):
        self.N = N
        self.cnt = 0
        self.mutex = Mutex()
        self.items = [0] * N
        self.free = self.items
        self.sem = Semaphore(0)

def producent (shared):
    # pristup k zdielanym premennym
    # produkcia ,chceme aby vyprodukoval polozku
    sleep(randint(0, 10) / 10)
    # kontrola volneho miesta v sklade
    shared.free.wait()
    # ziskanie vylucneho pristupu do skladu
    shared.mutex.lock()
    # ulozenie vyrobku do skladu
    sleep(randint(0, 1) / 10)
    # odidenie zo skladu
    shared.mutex.unlock()
    # zvysenie poctu vyrobku v sklade
    shared.items.signal()

def consumer (shared):
    # kontrola existencie vyrobku na sklade
    shared.items.wait()
    # ziskanie pristupu do skladu
    shared.mutex.lock()
    # ziskanie vyrobku, simulacia
    sleep(randint(0, 1) / 10)
    # odidenie zo skladu
    shared.mutex.unlock()
    # spracovanie vyrobku, simulacia
    sleep(randint(0, 10) / 10)

def stack_example(ls, shared, thread_index):

    while True:
        ls.lock(shared.sem)
        print('%d ' % ls.cnt)
        producent(shared)
        consumer(shared)
        ls.unlock(shared.sem)

thread_num = 5
shared = Shared(10)
ls = LightSwitch()

for x in range(thread_num):
    thread = Thread(sklad_example,ls, shared, x)