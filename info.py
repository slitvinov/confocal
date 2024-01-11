import tifffile
import sys
import re

while True:
    try:
        path = input()
    except EOFError:
        break
    tif = tifffile.TiffFile(path)
    nz = len(tif.pages)
    ny, nx = tif.pages[0].shape
    print("%s %d %d %d" % (re.sub("^\./", "", path), nx, ny, nz))
