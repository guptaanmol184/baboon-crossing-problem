#! /usr/bin/env python3

"""
Baboon Crossing problem
====== ======== =======

    Baboons can cross the canyon by swinging hand-over-hand on the rope, but if two baboons going in
    opposite directions meet in the middle, they will fight and drop to their deaths.
    Furthermore, the rope is only strong enough to hold 5 baboons. If there are
    more baboons on the rope at the same time, it will break.

    The following properties are ensured:

        1. Once a baboon has begun to cross, it is guaranteed to get to the other
           side without running into a baboon going the other way.

        2. There are never more than 5 baboons on the rope.

        3. A continuing stream of baboons crossing in one direction should not bar
	   baboons going the other way indefinitely (no starvation).
"""

import threading
import random
import time

max_on_rope = 5
left_baboon_count = 0
right_baboon_count = 0

class Lightswitch:
    def __init__(self):
        self.counter = 0
        self.mutex = threading.Semaphore(1)

    def lock(self, semaphore):
        self.mutex.acquire()
        self.counter += 1
        if self.counter == 1:
            semaphore.acquire()
        self.mutex.release()

    def unlock(self, semaphore):
        self.mutex.acquire()
        self.counter -= 1
        if self.counter == 0:
            semaphore.release()
        self.mutex.release()

# semaphore declarations
empty = threading.Semaphore(1)
left_switch = Lightswitch()
right_switch = Lightswitch()
left_multiplex = threading.Semaphore(max_on_rope)
right_multiplex = threading.Semaphore(max_on_rope)
turnstile = threading.Semaphore(1)

# worker functions
def left_baboon_go():
    turnstile.acquire()
    #print('baboon {} in waiting to get on to rope.'.format(threading.current_thread().getName()))
    left_switch.lock(empty)
    turnstile.release()

    left_multiplex.acquire()
    # cross the canyon
    print('->baboon {} got on to the rope.'.format(threading.current_thread().getName()))
    time.sleep(3)
    left_multiplex.release()
    print('->baboon {} got off the rope.'.format(threading.current_thread().getName()))

    left_switch.unlock(empty)

def right_baboon_go():
    turnstile.acquire()
    #print('baboon {} in waiting to get on to rope.'.format(threading.current_thread().getName()))
    right_switch.lock(empty)
    turnstile.release()

    right_multiplex.acquire()
    # cross the canyon
    print('->baboon {} got on to the rope.'.format(threading.current_thread().getName()))
    time.sleep(3)
    right_multiplex.release()
    print('->baboon {} got off the rope.'.format(threading.current_thread().getName()))

    right_switch.unlock(empty)

def main():
    print("Enter number of left baboons: ", end='')
    left_baboon_count = int(input())
    print("Enter number of right baboons: ", end='')
    right_baboon_count = int(input())

    threads = []
    for i in range(left_baboon_count):
        tname = 'l' + str(i)
        t = threading.Thread(name=tname, target=left_baboon_go)
        threads.append(t)
    
    for i in range(right_baboon_count):
        tname = 'r' + str(i)
        t = threading.Thread(name=tname, target=right_baboon_go)
        threads.append(t)

    # shuffle threads
    random.shuffle(threads)

    # start threads
    for i in range(len(threads)):
        threads[i].start()

    for i in range(len(threads)):
        threads[i].join()

if __name__ == "__main__":
    main()

                

