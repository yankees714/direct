#!/usr/bin/python
import Image
import glob
import os

pics = glob.glob('*')
pics_to_del = list()

for pic in pics:
    try:
        im=Image.open(pic)
    except IOError:
        os.system("mv "+pic+" ./trash")
    