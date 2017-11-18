from visual import *

tex = materials.texture( data = materials.loadTGA("rope"), mapping = "spherical")

sphere(pos = (0, 2, 0), material = tex)
cylinder(pos = (0,0,0), length = 10, material = tex)
box(pos = (0, -2, 0), material = tex)
