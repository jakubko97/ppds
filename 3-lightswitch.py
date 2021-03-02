from fei.ppds import Mutex
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