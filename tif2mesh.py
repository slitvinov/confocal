import numpy as np
import os
import re
import sys
import tifffile
import skimage.measure

Cell = False
level = 50
for path in sys.argv[1:]:
    basename = re.sub("\.tif$", "", os.path.basename(path))
    try:
        input = tifffile.TiffFile(path)
    except (FileNotFoundError, tifffile.tifffile.TiffFileError) as e:
        sys.stderr.write("tiff2mesh: %s\n" % e)
        sys.exit(1)
    dtype = input.pages[0].dtype
    nz = len(input.pages)
    ny, nx = input.pages[0].shape
    volume = np.ndarray((nx, ny, nz), dtype)
    for i, page in enumerate(input.pages):
        np.copyto(volume[:, :, i], page.asarray(), "no")
    verts, faces, normals, values = skimage.measure.marching_cubes(
        volume, level)
    off = "%s.off" % basename
    with open(off, "w") as f:
        f.write("OFF\n%ld %ld 0\n" % (len(verts), len(faces)))
        for x, y, z in verts:
            f.write("%.16e %.16e %.16e\n" % (x, y, z))
        for i, j, k in faces:
            f.write("3 %ld %ld %ld\n" % (i, j, k))
    sys.stderr.write("tiff2mesh: %s\n" % off)
