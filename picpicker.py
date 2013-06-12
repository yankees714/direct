#!/usr/bin/python
import Image
import glob
import os

pics = glob.glob('pics/*')
pics_to_del = list()

for pic in pics:
    try:
        im=Image.open(pic)
    except IOError:
        os.system("rm "+pic)
    else:
        size = im.size
        origWide = size[0]
        origHeig = size[1]
        newWide = 300
        newHeig = int(origHeig*(float(newWide)/float(origWide)))
        newSize = (newWide, newHeig)
        smaller = im.resize(newSize, Image.ANTIALIAS)
        smaller.save("oracleapp/assets/img/"+pic, "JPEG")
