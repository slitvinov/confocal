<h2>Analysis of red cell cofocal images</h2>

<h3>References</h3>

Simionato, G., Hinkelmann, K., Chachanidze, R., Bianchi, P., Fermo,
E., van Wijk, R., ... & Quint, S. (2021). Red blood cell phenotyping
from 3D confocal images using artificial neural networks. PLoS
computational biology, 17(5), e1008934.

<https://github.com/kgh-85/cytoShapeNet>

<h3>Install</h3>

<pre>
$ python -m pip install --no-deps tifffile
</pre>

<h3>Data</h3>

<https://zenodo.org/records/4670205>

Download 10Gb of data
<pre>
$ for i in 01 02 03 04 05 06 07 08 09 10
do wget -q https://zenodo.org/records/4670205/files/data.7z.0$i
done
</pre>

Extract files
<pre>
$ 7z x -bd data.7z.001
</pre>

<h3>Convert</h3>

<pre>
$ python tif2xdmf.py ref/000137.tif
tiff2xdmf: 101x101x185le.000137.raw
tiff2xdmf: 000137.xdmf2
</pre>
