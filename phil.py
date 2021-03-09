from time import sleep
from random import randint
from fei.ppds import Semaphore, print, Thread

PHIL_NUM = 5

def phil(forks, phil_id, fork1, fork2):
    sleep(randint(40,50)/1000)
    while True:
        think(phil_id)
        getForks(forks, phil_id, fork1, fork2)
        eat(phil_id)
        putForks(forks, phil_id, fork1, fork2)

def think(phil_id):
    print(f'{phil_id:02d}: thinking')
    sleep(randint(40,50)/1000)

def eat(phil_id):
    print(f'{phil_id:02d}: eating')
    sleep(randint(40,50)/1000)

def getForks(forks, phil_id, fork1, fork2):
    print(f'{phil_id:02d}: try to get forks')
    forks[fork1].wait()
    sleep(randint(40,50)/1000)
    forks[fork2].wait()
    print(f'{phil_id:02d}: taken forks')

def putForks(forks, phil_id, fork1, fork2):
    print(f'{phil_id:02d}: try to put forks')
    forks[fork1].signal()
    forks[fork2].signal()
    print(f'{phil_id:02d}: put forks')

def main():
    forks = [Semaphore(1) for _ in range(PHIL_NUM)]

    # phils = [Thread(phil, forks, p_id, p_id, (p_id+1) % PHIL_NUM) for p_id in range(PHIL_NUM)]

    phils = []
    for phil_id in range(PHIL_NUM):
        is_leftie = randint(0,1)
        lefties = 0
        if is_leftie:
            lefties += 1
            if lefties == PHIL_NUM:
                is_leftie = 0

        if is_leftie:
            phils.append(Thread(phil, forks, phil_id, (phil_id+1) % PHIL_NUM, phil_id))
        else:
            phils.append(Thread(phil, forks, phil_id, phil_id, (phil_id+1) % PHIL_NUM))

    for p in phils:
        p.join()

if __name__ == '__main__':
    main()