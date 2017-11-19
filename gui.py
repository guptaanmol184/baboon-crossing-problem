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

# GUI imports
from __future__ import division, print_function
from visual import *
from pygame import mixer # Load the required library
import Image

# threading imports
import threading
import random

###########################################################
# USER SETTINGS (Configure to your needs)
###########################################################

# maximum number of baboons at a time on the rope
max_on_rope = 5 
# number of baboons spawned on the rope on left
left_baboon_count = 15
# number of baboons spawned on the rope on right
right_baboon_count = 15

# MUSIC SETTINGS
mixer.init()
# uncomment to select music
#mixer.music.load('songs/five-little-mokeys.mp3')
mixer.music.load('songs/mowgli-sahara-theme.mp3')
#mixer.music.load('songs/monkey.mp3')
mixer.music.play()

###########################################################
# USER SETTINGS END $
###########################################################

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

#create tree function
def create_tree(pos):
    f = frame()
    f.pos =pos

    tree = cylinder(frame = f,pos = (0,0,0), length = 10, radius = 1, material = materials.wood,axis = (0,1,0))
    leafl = cone(frame = f,pos= (0,5,0), length = 8, radius = 3, color = color.green ,axis = (0,1,0))
    leafl = cone(frame = f,pos= (0,7.5,0), length = 5, radius = 2.5, color = color.green ,axis = (0,1,0))
    leafl = cone(frame = f,pos= (0,10,0), length = 5, radius = 2, color = color.green ,axis = (0,1,0))


def create_label(inp):
    lab = text(pos = (0,8,-7),text=inp[0], align='center', depth=-0.3)
    return lab

# box.size = (lenght(x), height(y), width(z))
#background wall
tex = materials.texture( data = materials.loadTGA("textures/sky"))
wall = box(pos = (0,0,-20),size=(90,50,1),material = tex, mapping='sign')
# Left platform
lf_plat = box(pos = (-20,-10,0), size = (20, 10, 20), material = materials.rough,color =groud_color)
# Right platform
rt_plat = box(pos = (20,-10,0), size = (20, 10, 20), material = materials.rough, color= groud_color) 
# Rope
rope_texture = materials.texture( data = materials.loadTGA("textures/rope.tga"),mapping='spherical')
rope = cylinder(pos = (-10,-6,0), length = 20, radius = 1, material = rope_texture)
#tree
create_tree((26,-6,-7))
create_tree((-26,-6,-7))
create_tree((-20,-6,-7))
create_tree((20,-6,-7))
create_tree((-14,-6,-7))
create_tree((14,-6,-7))
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

# lightswitch is used control the turn of left and right monkeys
class Lightswitch:
    def __init__(self):
        self.counter = 0
        self.mutex = threading.Semaphore(1)
        self.dir_arr = arrow(pos = (0,-5,5), visible=False)

    # dir 1 = right -1 = left
    def lock(self, semaphore, dir):
        self.mutex.acquire()
        self.counter += 1
        if self.counter == 1:
            semaphore.acquire()
            self.gui_arr_show(dir)
        self.mutex.release()

    def unlock(self, semaphore):
        self.mutex.acquire()
        self.counter -= 1
        if self.counter == 0:
            semaphore.release()
            self.gui_arr_hide()
        self.mutex.release()

    def gui_arr_show(self, dir):
        if dir == 1:
            self.dir_arr.color = color.red
            self.dir_arr.axis = (-6, 0,0)
        elif dir == -1:
            self.dir_arr.color = color.orange
            self.dir_arr.axis = (6, 0,0)
        self.dir_arr.visible = True

    def gui_arr_hide(self):
        self.dir_arr.visible = False

# semaphore declarations
empty = threading.Semaphore(1)
left_switch = Lightswitch()
right_switch = Lightswitch()
left_multiplex = threading.Semaphore(max_on_rope)
right_multiplex = threading.Semaphore(max_on_rope)
turnstile = threading.Semaphore(1)

# global position declarations
# left position start
lt_pos = -11
# left potion next coordinate
lt_inc = -1
# right position start
rt_pos = 11
# right potion next coordinate
rt_inc = 1

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
    return arrow(pos = (lt_pos, -5, 0), axis=(0,5,0), color = color.orange)

def rt_baboon_create():
    global rt_pos
    global rt_inc
    # increment pos
    rt_pos = rt_pos + rt_inc
    return arrow(pos = (rt_pos, -5, 0), axis=(0,5,0), color = color.red)

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
        if(arr.x > 30 or arr.x < -30):
            break 
        if(i==20):
            break
        i+=1
        rate(5)

###########################################################
# GUI FUNCTIONS END $
###########################################################

###########################################################
# THREAD WORKER FUNCTIONS
###########################################################

# worker functions
def left_baboon_go(baboon):
    #inp=['left','green']
    turnstile.acquire()
    #print('baboon {} in waiting to get on to rope.'.format(threading.current_thread().getName()))
    left_switch.lock(empty, -1)
    #create_label(inp)
    turnstile.release()

    left_multiplex.acquire()
    # cross the canyon
    print('->baboon {} got on to the rope.'.format(threading.current_thread().getName()))
    while baboon.x < 11:
        rate(10)
        baboon.pos.x+=1
    #baboon.visible = False
    left_multiplex.release()


    left_switch.unlock(empty)
    
    while baboon.pos.z<8:
        rate(10)
        baboon.pos.z+=1 
    baboon_jump(baboon)              
    baboon.visible = False

def right_baboon_go(baboon):
    turnstile.acquire()
    #print('baboon {} in waiting to get on to rope.'.format(threading.current_thread().getName()))
    right_switch.lock(empty, 1)
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

    
    while baboon.pos.z<8:
        rate(10)
        baboon.pos.z+=1 
    baboon_jump(baboon)              
    baboon.visible = False

###########################################################
# THREAD WORKER FUNCTIONS END $
###########################################################


###########################################################
# MAIN RUNNER ROUTINE
###########################################################

def main():
    threads = []
    for i in range(left_baboon_count):
        l_gui = lt_baboon_create()
        tname = 'l' + str(i)
        t = threading.Thread(name=tname, target=left_baboon_go, args = (l_gui,))
        threads.append(t)

    for i in range(right_baboon_count):
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

###########################################################
# MAIN RUNNER ROUTINE END $
###########################################################

# Call main
if __name__ == '__main__':
    main()

