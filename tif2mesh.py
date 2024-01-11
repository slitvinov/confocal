import numpy as np
import os
import re
import sys
import tifffile
import skimage.measure
import struct

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
    sys.stdout.buffer.write(b"OFF BINARY\n")
    sys.stdout.buffer.write(struct.pack(">3i", len(verts), len(faces), 0))
    for x, y, z in verts:
        sys.stdout.buffer.write(struct.pack(">3f", x, y, z))
    for i, j, k in faces:
        sys.stdout.buffer.write(struct.pack(">5i", 3, i, j, k, 0))
