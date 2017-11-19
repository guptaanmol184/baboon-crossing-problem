#! /usr/bin/env python3

# GUI imports
from __future__ import division, print_function
from visual import *
from pygame import mixer # Load the required library
import Image

# threading imports
import threading
import random

###########################################################
# BASE GUI
###########################################################

################################################
# SCENE DEFINATION
################################################
# set light blue background
# scene.background = (0, 50, 100)
# set 16:9 aspect ration of the screen
scene.width = 1200
scene.height = 675
#scene.autoscale = False
scene.range = (30,40,30)
scene.forward = (0, -0.5, -1)

################################################
# LANDSCPAE DEFINATION
################################################

groud_color = (139/255,69/255,19/255)




# box.size = (lenght(x), height(y), width(z))
#background wall
tex = materials.texture( data = materials.loadTGA("textures/sky"))
wall = box(pos = (0,0,-20),size=(90,50,1),material = tex, mapping='sign')
#wall.rotate(angle=pi/2,origin=pos,axis=(0,1,0))
# Left platform
lf_plat = box(pos = (-20,-10,0), size = (20, 10, 20), material = materials.rough,color =groud_color)
# Right platform
rt_plat = box(pos = (20,-10,0), size = (20, 10, 20), material = materials.rough, color= groud_color) 
# Rope
rope_texture = materials.texture( data = materials.loadTGA("textures/rope.tga"),mapping='spherical')
rope = cylinder(pos = (-10,-6,0), length = 20, radius = 1, material = rope_texture)
#tree
treel = cylinder(pos = (-15,-6,-5), length = 10, radius = 1, material = materials.wood,axis = (0,1,0))
treer = cylinder(pos = (15,-6,-5), length = 10, radius = 1, material = materials.wood,axis = (0,1,0))
#leaves
leafl1 = cone(pos= (-15,1,-5), length = 8, radius = 3, color = color.green ,axis = (0,1,0))
leafl2 = cone(pos= (-15,4,-5), length = 5, radius = 2.5, color = color.green ,axis = (0,1,0))
leafr1 = cone(pos= (15,1,-5), length = 8, radius = 3, color = color.green ,axis = (0,1,0))
leafr2 = cone(pos= (15,4,-5), length = 5, radius = 2.5, color = color.green ,axis = (0,1,0))
#ground
ground = box(pos = (0,-15,0), size = (60,1,20), material = materials.rough, color = groud_color)
#water
water = box(pos = (0,-11.5,0), size = (20,7,20), material = materials.rough, color = color.blue)


###########################################################
# BASE GUI END $
###########################################################

###########################################################
# HELPERS
###########################################################

max_on_rope = 5
left_baboon_count = 10
right_baboon_count = 10

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

# global position declarations
lt_pos = -11
lt_inc = -1
rt_pos = 11
rt_inc = 1

class rt_monkey:
    def __init__(self, x):
        self.arr = arrow(pos = (x, -5, 0), axis=(0,5,0), color = color.red)

    def go(self):
        while self.arr.x > -11:
            rate(1)
            self.arr.x+=1
        #self.disappear()

    def disappear(self):
        self.arr.visible = False

class lt_monkey:
    def __init__(self, x):
        self.arr = arrow(pos = (x, -5, 0), axis=(0,5,0), color = color.cyan)

    def go(self):
        while self.arr.x < 11:
            print('gonna go')
            self.arr.x+=1
        #self.disappear()

    def disappear(self):
        self.arr.visible = False

###########################################################
# HELPERS END $
###########################################################

###########################################################
# GUI FUNCTIONS
###########################################################

def lt_baboon_create():
    global lt_pos
    global lt_inc
    # increment pos
    lt_pos = lt_pos + lt_inc
    return arrow(pos = (lt_pos, -5, 0), axis=(0,5,0), color = color.green)

def rt_baboon_create():
    global rt_pos
    global rt_inc
    # increment pos
    rt_pos = rt_pos + rt_inc
    return arrow(pos = (rt_pos, -5, 0), axis=(0,5,0), color = color.red)

def lt_gui_go(arr):
    while arr.x < 11:
        rate(1)
        arr.x+=1

def rt_gui_go():
    while arr.x > -11:
        rate(1)
        arr.x-=1

def baboon_jump(arr):
    i=0
    while True:
        if i%2==0:
            arr.pos.y=arr.pos.y+1
        else:
            arr.pos.y=arr.pos.y-1
        arr.pos = arr.pos + (random.randint(-1,1),0,0)                
        
        # left and reight
        if((arr.x > 0 and arr.x < 10) or (arr.x > -10 and arr.x < 0)):
            break 
        # left and right
       # if((arr.x > 0 and arr.x < 10) or (arr.x > -10 and arr.x < 0)):
#        if i == 6:
#            break
        i+=1
        rate(5)


###########################################################
# GUI FUNCTIONS END $
###########################################################


# worker functions
def left_baboon_go(baboon):
    turnstile.acquire()
    #print('baboon {} in waiting to get on to rope.'.format(threading.current_thread().getName()))
    left_switch.lock(empty)
    turnstile.release()

    left_multiplex.acquire()
    # cross the canyon
    print('->baboon {} got on to the rope.'.format(threading.current_thread().getName()))
    while baboon.x < 11:
        rate(10)
        baboon.pos.x+=1
    #baboon.visible = False
    left_multiplex.release()
    print('->baboon {} got off the rope.'.format(threading.current_thread().getName()))

    left_switch.unlock(empty)
    
    while baboon.pos.z>-8:
        rate(10)
        baboon.pos.z-=1 
    baboon_jump(baboon)              
    baboon.visible = False

def right_baboon_go(baboon):
    turnstile.acquire()
    #print('baboon {} in waiting to get on to rope.'.format(threading.current_thread().getName()))
    right_switch.lock(empty)
    turnstile.release()

    right_multiplex.acquire()
    # cross the canyon
    print('->baboon {} got on to the rope.'.format(threading.current_thread().getName()))
    while baboon.x > -11:
        rate(10)
        baboon.pos.x-=1
    #baboon.visible = False
    right_multiplex.release()
    print('->baboon {} got off the rope.'.format(threading.current_thread().getName()))

    right_switch.unlock(empty)

    
    while baboon.pos.z>-8:
        rate(10)
        baboon.pos.z-=1 
    baboon_jump(baboon)              
    baboon.visible = False
#print("Enter number of left baboons: ")
#left_baboon_count = int(input())
#print("Enter number of right baboons: ")
#right_baboon_count = int(input())

threads = []

mixer.init()
mixer.music.load('Five - Little.mp3')
#mixer.music.load('zoo.mp3')
mixer.music.play()

for i in range(left_baboon_count):
    #lt_pos = lt_pos + lt_inc
    #l_gui = lt_monkey(lt_pos)
    l_gui = lt_baboon_create()
    tname = 'l' + str(i)
    t = threading.Thread(name=tname, target=left_baboon_go, args = (l_gui,))
    threads.append(t)

for i in range(right_baboon_count):
#   rt_pos = rt_pos + rt_inc
    #r_gui = rt_monkey(rt_pos)
    r_gui = rt_baboon_create()
    tname = 'r' + str(i)
    t = threading.Thread(name=tname, target=right_baboon_go, args = (r_gui,))
    threads.append(t)

# shuffle threads
random.shuffle(threads)
 
# start threads
for i in range(len(threads)):
    threads[i].start()

for i in range(len(threads)):
    threads[i].join()

