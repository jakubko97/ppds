"""
N – max. počet zákazníkov (N-1 v čakárni, 1 v kresle)
customers – aktuálny počet zákazníkov v holičstve
mutex – chráni integritu počítadla „customers‟
customer – holič čaká na zákazníka, pokým nepríde do holičstva
barber – po príchode do holičstva čaká zákazník na holiča, kým
ho tento nezavolá na kreslo
customerDone a barber Done – po skončení holenia zákazník
signalizuje „customerDone‟ a čaká na „barberDone‟
"""

from random import randint
from time import sleep
from fei.ppds import print, Thread, Mutex, Semaphore

N = 5

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

def barber(barber_id ,shared):
    while True:
        shared.customer.wait()
        shared.barber.signal()

        cutHair(barber_id)

        shared.customerDone.wait()
        shared.barberDone.signal()

def balk(customer_id):
    print(f"Customer {customer_id} : leaving")
    sleep(randint(0,2)/10)

def getHairCut(customer_id):
    print(f"Customer {customer_id} : getting haircut")
    sleep(2/10 + 0.4)

def cutHair(barber_id):
    print(f"Barber {barber_id} : cutting hair")
    sleep(2/10 + 0.4)

def customer(customer_id, shared):
    while True:
        if shared.customers == N:
            balk(customer_id)
        shared.customers +=1

        shared.customer.signal()
        shared.barber.wait()

        shared.customerDone.signal()
        shared.barberDone.wait()

        shared.customers -= 1

class Shared(object):
    def __init__(self):
        self.barberDone = Semaphore(0)
        self.customerDone = Semaphore(0)
        self.barber = Semaphore(0)
        self.mutex = Mutex()
        self.customers = 0
        self.customer = Semaphore(0)


s = Shared()
barber = [Thread(barber, i ,s) for i in range(1)]
customer = [Thread(customer, i, s) for i in range(N)]
for p in barber + customer:
    p.join()