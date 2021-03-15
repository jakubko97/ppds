import time
from random import randint
from time import sleep
from fei.ppds import Thread, Semaphore, Mutex, Event, print


class LightSwitch():
    def __init__(self):
        self.mutex = Mutex()
        self.counter = 0

    def lock(self, semaphore):
        self.mutex.lock()
        counter = self.counter
        self.counter += 1
        if self.counter == 1:
            semaphore.wait()
        self.mutex.unlock()
        return counter

    def unlock(self, semaphore):
        self.mutex.lock()
        self.counter -= 1
        if self.counter == 0:
            semaphore.signal()
        self.mutex.unlock()


def init():
    access_data = Semaphore(1)
    turniket = Semaphore(1)
    ls_monitor = LightSwitch()
    ls_cidlo = LightSwitch()
    valid_data = Event()

    for monitor_id in range(2):
        Thread(monitor, monitor_id, valid_data, turniket, ls_monitor,
               access_data)

    for cidlo_id in range(11):
        Thread(cidlo, cidlo_id, valid_data, turniket, ls_cidlo, access_data)


def monitor(monitor_id, valid_data, turniket, ls_monitor, access_data):
    valid_data.wait()

    while True:
        sleep(.5)
        turniket.wait()
        pocet_citajucich_monitorov = ls_monitor.lock(access_data)
        turniket.signal()

        print(
            f'monit "{monitor_id:02d}": pocet_citajucich_monitorov={pocet_citajucich_monitorov:02d}'
        )

        ls_monitor.unlock(access_data)


def cidlo(cidlo_id, valid_data, turniket, ls_cidlo, access_data):
    while True:
        turniket.wait()
        turniket.signal()

        pocet_zapisujucich_cidiel = ls_cidlo.lock(access_data)
        trvanie_zapisu = randint(10, 15) / 1000
        print(
            f'cidlo "{cidlo_id:02d}":  pocet_zapisujucich_cidiel={pocet_zapisujucich_cidiel:02d}, trvanie_zapisu={trvanie_zapisu:5.3f}'
        )
        sleep(trvanie_zapisu)
        valid_data.signal()
        ls_cidlo.unlock(access_data)


if __name__ == '__main__':
    init()
