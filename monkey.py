from base import *

class rt_monkey:
    def __init__(self, x):
        self.arr = arrow(pos = (x, -5, 0), axis=(0,5,0), color = color.red)

    def go(self):
        while self.arr.x < 11:
            rate(10)
            self.arr.x+=1
        self.disappear()

    def disappear(self):
        self.arr.visible = False

class lf_monkey:
    def __init__(self, x):
        self.arr = arrow(pos = (x, -5, 0), axis=(0,5,0), color = color.green)

    def go_left(self):
        while self.arr.x > -11:
            rate(10)
            self.arr.x+=1

    def disappear(self):
        self.arr.visible = False

a = []
for i in range(-12, -22, -1):
    temp = rt_monkey(i)
    a.append(temp)

for i in range(len(a)):
    a[i].go()

