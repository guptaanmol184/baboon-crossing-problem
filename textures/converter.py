from visual import *
from PIL import Image # Must install PIL
name = "sky" # PUT IMAGE NAME WITH OUT EXTENSION HERE (.JPG ONLY)
width = 4096 # must be power of 2
height = 256 # must be power of 2
im = Image.open(name+".jpg")
#print(im.size) # optionally, see size of image
# Optional cropping:
#im = im.crop((x1,y1,x2,y2)) # (0,0) is upper left
im = im.resize((width,height), Image.ANTIALIAS)
materials.saveTGA(name,im)
