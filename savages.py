"""Riesenie modifikovaneho problemu divochov."""

from fei.ppds import Semaphore, Mutex, Thread, print
from random import randint
from time import sleep

"""M a N su parametre modelu, nie synchronizacie ako takej.
Preto ich nedavame do zdielaneho objektu.
    M - pocet porcii misionara, ktore sa zmestia do hrnca.
    N - pocet divochov v kmeni (kuchara nepocitame).
    C - pocet kucharov
    P - pocet porcii, ktory spravi kuchar na striedacku s druhym
"""
M = 3
N = 3
C = 2
P = 1

class SimpleBarrier:

    def __init__(self, N):
        self.N = N
        self.mutex = Mutex()
        self.cnt = 0
        self.sem = Semaphore(0)

    def wait(self,
             print_str,
             human_id,
             print_last_thread=False,
             print_each_thread=False):
        self.mutex.lock()
        self.cnt += 1
        if print_each_thread:
            print(print_str % (human_id, self.cnt))
        if self.cnt == self.N:
            self.cnt = 0
            if print_last_thread:
                print(print_str % (human_id))
            self.sem.signal(self.N)
        self.mutex.unlock()
        self.sem.wait()


class Shared:

    def __init__(self):
        self.mutex = Mutex()
        self.servings = 0
        self.full_pot = Semaphore(0)
        self.empty_pot = Semaphore(0)
        self.barrier1 = SimpleBarrier(N)
        self.barrier2 = SimpleBarrier(N)
        self.barrier3 = SimpleBarrier(C)
        self.barrier4 = SimpleBarrier(C)


def get_serving_from_pot(savage_id, shared):
    # Pristupujeme ku zdielanej premennej.
    # Funkcia je volana pri zamknutom mutexe, preto netreba
    # riesit serializaciu v ramci samotnej funkcie.

    print("divoch %2d: beriem si porciu" % savage_id)
    shared.servings -= 1


def eat(savage_id):
    print("divoch %2d: hodujem" % savage_id)
    # Zjedenie porcie misionara nieco trva...
    sleep(0.2 + randint(0, 3) / 10)


def savage(savage_id, shared):
    while True:

        shared.barrier1.wait(
            "divoch %2d: prisiel som na veceru, uz nas je %2d",
            savage_id,
            print_each_thread=True)
        shared.barrier2.wait("divoch %2d: uz sme vsetci, zaciname vecerat",
                             savage_id,
                             print_last_thread=True)

        # Nasleduje klasicke riesenie problemu hodujucich divochov.
        shared.mutex.lock()
        print("divoch %2d: pocet zostavajucich porcii v hrnci je %2d" %
              (savage_id, shared.servings))
        if shared.servings == 0:
            print("divoch %2d: budim kuchara" % savage_id)
            shared.empty_pot.signal(C)
            shared.full_pot.wait()
        get_serving_from_pot(savage_id, shared)
        shared.mutex.unlock()

        eat(savage_id)

def put_servings_in_pot(cook_id, shared):

    print("kuchar %2d: varim" % cook_id)
    # navarenie jedla tiez cosi trva...
    sleep(0.4 + randint(0, 2) / 10)
    shared.servings += P

def cook(cook_id, M, shared):

    while True:

        shared.empty_pot.wait()
        shared.barrier3.wait(
            "kuchar %2d: prisiel som uvarit, uz nas je %2d",
            cook_id,
            print_each_thread=True)
        shared.barrier4.wait("kuchar %2d: uz sme vsetci, zaciname varit",
                             cook_id,
                             print_last_thread=True)
        shared.mutex.lock()
        if shared.servings == M:
            print("kuchar %2d: je navarene, budim divocha" % cook_id)
            shared.full_pot.signal()
        shared.mutex.unlock()
        put_servings_in_pot(cook_id, shared)


def init_and_run(N, M):
    """Spustenie modelu"""
    savages = list()
    cooks = list()
    shared = Shared()
    for savage_id in range(0, N):
        savages.append(Thread(savage, savage_id, shared))
    for cook_id in range(0, C):
        cooks.append(Thread(cook,cook_id, M, shared))

    for t in savages + cooks:
        t.join()


if __name__ == "__main__":
    init_and_run(N, M)