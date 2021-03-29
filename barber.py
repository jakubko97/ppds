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
from fei.ppds import print, Thread, Mutex, Semaphore, Event

class Shared(object):
    def __init__(self, N):
        self.N = N
        self.barberDone = Semaphore(0)
        self.customerDone = Semaphore(0)
        self.mutex = Mutex()
        self.customers = 0
        self.customer = Semaphore(0)

        self.queue = []

def barber(barber_id, shared):
    while True:

        shared.customer.wait()
        shared.mutex.lock()
        barber = shared.queue.pop(0)
        shared.mutex.unlock()

        barber.signal()

        cutHair(barber_id)

        shared.customerDone.wait()
        shared.barberDone.signal()

def balk(customer_id):
    print(f"Customer {customer_id} : balk.")
    sleep(.1)

def getHairCut(customer_id):
    print(f"Customer {customer_id} : getting haircut.")
    sleep(randint(2,4)/100)

def cutHair(barber_id):
    print(f"Barber {barber_id}: cutting hair.")
    sleep(randint(2,4)/100)

def customerExit(customer_id):
    print(f"Customer {customer_id}: exited.")
    sleep(randint(1,2)/100)

def customerEnter(customer_id):
    print(f"Customer {customer_id}: entered.")
    sleep(randint(9,10)/100)

def customer(customer_id, shared):
    barber = Semaphore(0)

    while True:
        shared.mutex.lock()
        customerEnter(customer_id)
        if shared.customers == shared.N:
            balk(customer_id)
            shared.mutex.unlock()
        else:
            shared.customers +=1
            shared.queue.append(barber)
            shared.mutex.unlock()

            shared.customer.signal()
            barber.wait()

            getHairCut(customer_id)

            shared.customerDone.signal()
            shared.barberDone.wait()

            shared.mutex.lock()
            shared.customers -= 1
            customerExit(customer_id)
            shared.mutex.unlock()

def run_model():

    s = Shared(5)
    b = [Thread(barber, i, s) for i in range(2)]
    c = [Thread(customer, i, s) for i in range(10)]


if __name__ == "__main__":
    run_model()
