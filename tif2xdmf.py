import numpy as np
import os
import re
import sys
import tifffile

Cell = False
for path in sys.argv[1:]:
    basename = re.sub("\.tif$", "", os.path.basename(path))
    try:
        input = tifffile.TiffFile(path)
    except (FileNotFoundError, tifffile.tifffile.TiffFileError) as e:
        sys.stderr.write("tiff2xdmf: %s\n" % e)
        sys.exit(1)
    dtype = input.pages[0].dtype
    if dtype != np.dtype("uint8"):
        sys.stderr.write("tiff2xdmf: error: only dtype=uint8 is supported\n")
        sys.exit(1)

    nz = len(input.pages)
    ny, nx = input.pages[0].shape
    raw = "%dx%dx%dle.%s.raw" % (nx, ny, nz, basename)
    xdmf = "%s.xdmf2" % basename
    out = np.ndarray((nx, ny), dtype)
    with open(raw, "wb") as f:
        for page in input.pages:
            page.asarray(out=out)
            f.write(out.tobytes())
    with open(xdmf, "w") as f:
        f.write("""\
<Xdmf
    Version="2">
  <Domain>
    <Grid>
      <Topology
          TopologyType="3DCoRectMesh"
          Dimensions="%d %d %d"/>
      <Geometry
          GeometryType="ORIGIN_DXDYDZ">
        <DataItem
            Dimensions="3">
          0
          0
          0
        </DataItem>
        <DataItem
            Dimensions="3">
          1
          1
          1
        </DataItem>
      </Geometry>
      <Attribute
          Name="u"
          Center="%s">
        <DataItem
            NumberType="UChar"
            Format="Binary"
            Dimensions="%ld %ld %ld">
          %s
        </DataItem>
      </Attribute>
    </Grid>
  </Domain>
</Xdmf>
""" % ((nz + 1, ny + 1, nx + 1, "Cell", nz, ny, nx, raw) if Cell else
               (nz, ny, nx, "Node", nz, ny, nx, raw)))
    sys.stderr.write("tiff2xdmf: %s\n" % raw)
    sys.stderr.write("tiff2xdmf: %s\n" % xdmf)
