"""
pavian():
    strana = <0 ,1>
    while True:
        turn.wait()
        ls[strana].wait(som_lano)
        turn.signal()

        mplex.wait()
        ruckuj_po_lane()
        mplex.signal()

        ls[strana].signal(som_lano)

        strana := (strana +1 ) % 2
"""

from random import randint
from time import sleep
from fei.ppds import print, Thread, Mutex, Semaphore

def pavian(pid, shared):
    strana = randint(0, 1)
    while True:
        sleep(randint(0,4)/10 + 0.2)

        shared.turn_mutex.lock()
        shared.turn_cnt[strana] += 1
        print(f"turn {pid}: smer = {shared.smer} 0 = {shared.turn_cnt[0]}, 1 = {shared.turn_cnt[1]}")
        shared.turn_mutex.unlock()
        shared.turn.wait()
        shared.turn_mutex.lock()
        shared.turn_cnt[strana] -= 1
        shared.turn_mutex.unlock()
        shared.ls[strana].wait(shared.lano)
        shared.turn.signal()

        shared.mplex.wait()

        shared.mutex.lock()
        shared.lano_cnt += 1
        lano_cnt = shared.lano_cnt
        shared.mutex.unlock()

        ruckuj(pid, strana, lano_cnt)

        shared.mutex.lock()
        shared.lano_cnt -= 1
        shared.mutex.unlock()

        shared.mplex.signal()
        shared.ls[strana].signal(shared.lano)

        strana = (strana+1) % 2

def ruckuj(pid, strana, lano_cnt):
    print(f"{pid} ruckujem zo strany {strana} na lane nas je {lano_cnt}")
    sleep(randint(0,2)/10 + 0.4)

class LightSwitch(object):
    def __int__(self):
        self.cnt = 0
        self.mutex = Mutex()

    def wait(self, sem):
        self.mutex.lock()
        self.cnt += 1
        if self.cnt == 1:
            sem.wait()
        self.mutex.unlock()

    def signal(self, sem):
        self.mutex.lock()
        self.cnt -= 1
        if self.cnt == 0:
            sem.signal()
        self.mutex.unlock()

class Shared(object):
    def __init__(self):
        self.lano = Semaphore(1)
        self.mplex = Semaphore(5)
        self.ls = [LightSwitch(), LightSwitch()]
        self.turn = Semaphore(1)
        self.mutex = Mutex()
        self.lano_cnt = 0

        self.turn_mutex  = Mutex()
        self.turn_cnt = [0 , 0]
        self.smer = 0

s = Shared()
pav = [Thread(pavian, i, s) for i in range(10)]
for p in pav:
    p.join()