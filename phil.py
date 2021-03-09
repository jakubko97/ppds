from time import sleep
from random import randint
from fei.ppds import Semaphore, print, Thread

PHIL_NUM = 5

def phil(shared, footman, phil_id):
    while True:
        think(phil_id)
        getForks(shared, footman, phil_id)
        eat(phil_id)
        putForks(shared, footman, phil_id)

def think(phil_id):
    print(f'{phil_id:02d}: thinking')
    sleep(randint(40,50)/1000)

def eat(phil_id):
    print(f'{phil_id:02d}: eating')
    sleep(randint(40,50)/1000)

def getForks(forks, footman, phil_id):
    footman.wait()
    print(f'{phil_id:02d}: try to get forks')
    forks[phil_id].wait()
    forks[(phil_id +1) % PHIL_NUM].wait()
    print(f'{phil_id:02d}: taken forks')

def putForks(forks, footman, phil_id):
    print(f'{phil_id:02d}: try to put forks')
    forks[phil_id].signal()
    forks[(phil_id +1) % PHIL_NUM].signal()
    print(f'{phil_id:02d}: put forks')
    footman.signal()

def main():
    forks = [Semaphore(1) for _ in range(PHIL_NUM)]
    footman = Semaphore(PHIL_NUM-1)

    phils = [Thread(phil, forks,footman, p_id) for p_id in range(PHIL_NUM)]

    for p in phils:
        p.join()

if __name__ == '__main__':
    main()