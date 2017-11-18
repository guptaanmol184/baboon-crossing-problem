from __future__ import division, print_function
from visual import *

################################################
# DEFAUL CONSTANTS
################################################
origin_vector = vector(0,0,0)
unit_x = vector(1,0,0)
unit_y = vector(0,1,0)
unit_z = vector(0,0,1)

################################################
# SCENE DEFINATION
################################################
# set light blue background
# scene.background = (0, 50, 100)
# set 16:9 aspect ration of the screen
scene.width = 1200
scene.height = 675
# scene.autoscale = False

################################################
# LANDSCPAE DEFINATION
################################################

# box.size = (lenght(x), height(y), width(z))
# Left platform
lf_plat = box(pos = (-20,-10,0), size = (20, 10, 20), material = materials.wood)
# Right platform
rt_plat = box(pos = (20,-10,0), size = (20, 10, 20), material = materials.wood)
# Rope
rope_texture = materials.texture( data = materials.loadTGA("textures/rope.tga"), mapping = "spherical")
rope = cylinder(pos = (-10,-6,0), length = 20, radius = 1, material = rope_texture)
