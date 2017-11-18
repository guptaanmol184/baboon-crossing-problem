from visual import *

import threading
a = sphere(color = color.green)
b = sphere(pos =(5, -5, 0), color = color.green)

def run(a, i):
    if i == 1:
        a.radius = 20
    if i == 2:
        a.color = color.cyan
    if i == 3:
        while a.radius !=0:
            sleep(0.02)
            a.radius -=1
    if i == 4:
        while a.radius !=30:
            a.radius +=1

threads = []
for i in range(5):
    tname = 'l' + str(i)
    if i%2 == 0:
        t = threading.Thread(name=tname, target=run, args=(a, i))
    else:
        t = threading.Thread(name=tname, target=run, args=(b, i))
    threads.append(t)

# start threads
for i in range(len(threads)):
    threads[i].start()

for i in range(len(threads)):
    threads[i].join()
