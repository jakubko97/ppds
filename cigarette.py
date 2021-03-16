import time
from random import randint
from time import sleep
from fei.ppds import Thread, Semaphore, Mutex, Event, print


class Shared(object):
    def __init__(self):
        self.tobacco = Semaphore(0)
        self.paper = Semaphore(0)
        self.match = Semaphore(0)

        self.agentSem = Semaphore(1)

        self.isTobacco = 0
        self.isPaper = 0
        self.isMatch = 0
        self.mutex = Mutex()

        self.smokerMatch = Semaphore(0)
        self.smokerPaper = Semaphore(0)
        self.smokerTobacco = Semaphore(0)

def smoker_match(shared):
    while True:
        sleep(randint(0,10)/100)

        shared.paper.wait()
        print("\ts_M: paper")
        shared.tobacco.wait()
        print("\ts_M: tobacco")

        make_cigarette("smoker_match")
        shared.agentSem.signal()
        smoke("smoke_match")


def smoker_tobacco(shared):
    while True:
        sleep(randint(0,10)/100)

        shared.match.wait()
        print("\ts_M: match")
        shared.paper.wait()
        print("\ts_M: paper")

        make_cigarette("smoker_tobacco")
        shared.agentSem.signal()
        smoke("smoke_tobacco")

def smoker_paper(shared):
    while True:
        sleep(randint(0,10)/100)

        shared.match.wait()
        print("\ts_M: match")
        shared.tobacco.wait()
        print("\ts_M: tobacco")

        make_cigarette("smoker_paper")
        shared.agentSem.signal()
        smoke("smoke_paper")

def agent_1(shared):
    while True:
        sleep(randint(0,10)/100)

        # shared.agentSem.wait()
        print("agent: tobacco, paper")
        shared.tobacco.signal()
        shared.paper.signal()

def agent_2(shared):
    while True:
        sleep(randint(0,10)/100)

        # shared.agentSem.wait()
        print("agent: tobacco, paper")
        shared.paper.signal()
        shared.match.signal()

def agent_3(shared):
    while True:
        sleep(randint(0,10)/100)

        # shared.agentSem.wait()
        print("agent: tobacco, paper")
        shared.tobacco.signal()
        shared.match.signal()


def dealer_tobacco(shared):
    while True:
        shared.tobacco.wait()

        shared.mutex.lock()
        print("paper =  {shared.isPaper} , match =  {shared.isMatch} , tobacco =  {shared.isTobacco}")
        if shared.isPaper:
            shared.isPaper -= 1
            shared.smokerMatch.signal()
        elif shared.isMatch:
            shared.isMatch -= 1
            shared.smokerPaper.signal()
        else: shared.isTobacco += 1
    shared.mutex.unlock()

def dealer_match(shared):
    while True:
        shared.tobacco.wait()

        shared.mutex.lock()
        print(f"paper =  {shared.isPaper} , match =  {shared.isMatch} , tobacco =  {shared.isTobacco}")
        if shared.isPaper:
            shared.isPaper -= 1
            shared.smokerMatch.signal()
        elif shared.isTobacco:
            shared.isTobacco -= 1
            shared.smokerPaper.signal()
        else: shared.isMatch += 1
    shared.mutex.unlock()

def dealer_paper(shared):
    while True:
        shared.tobacco.wait()

        shared.mutex.lock()
        print(f"paper =  {shared.isPaper} , match =  {shared.isMatch} , tobacco =  {shared.isTobacco}")
        if shared.isMatch:
            shared.isMatch -= 1
            shared.smokerTobacco.signal()
        elif shared.isTobacco:
            shared.isTobacco -= 1
            shared.smokerMatch.signal()
        else: shared.isPaper += 1
    shared.mutex.unlock()

def make_cigarette(who):
    print(f"\tmakes cigarette: {who}")
    sleep(randint(0,10)/100)

def smoke(who):
    # print(f"\tsmokes: {who}")
    sleep(randint(0,10)/100)


def print_state(shared):
    shared.mutex.lok()
    print(f"paper =  {shared.isPaper+1} , match =  {shared.isMatch} , tobacco =  {shared.isTobacco}")

def run_model():
    shared = Shared()

    dealers = []
    dealers.append(Thread(dealer_match, shared))
    dealers.append(Thread(dealer_tobacco, shared))
    dealers.append(Thread(dealer_paper, shared))

    smokers = []
    smokers.append(Thread(smoker_match, shared))
    smokers.append(Thread(smoker_tobacco, shared))
    smokers.append(Thread(smoker_paper, shared))

    agents = []
    agents.append(Thread(agent_1, shared))
    agents.append(Thread(agent_2, shared))
    agents.append(Thread(agent_3, shared))

    for t in dealers + agents + smokers:
        t.join()

if __name__ == '__main__':
    run_model()