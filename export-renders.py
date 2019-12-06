"""
Python (v3.3) script for projecting pixel coordinates keyed by image into
3d-model space in Agisoft Photoscan Pro v1.
This script must be run from within Photoscan

Input file should be a GeoJSON in pixel coordinates.

Photoscan API usage from
[Export xyz coordinates of Markers]
  (http://www.agisoft.com/forum/index.php?topic=4121.msg21137#msg21137)
  - reply 4 from Alexey Pasumansky
"""

import sys
from os import path, environ
__dirname__ = path.dirname(__file__)
# Add local modules to path
sys.path.append(path.join(__dirname__,'modules'))

import fiona
import numpy as N
from matplotlib import pyplot as plt
from shapely.geometry import shape
from attitude import Orientation
from attitude.display.polar import pole, pole_error, uncertain_pole
from matplotlib import patches, image
from plot_colors import colors

image_file = sys.argv[1]
infile = sys.argv[2]
outfile = sys.argv[3]
dpi = 96

# reading png image file
im = image.imread(image_file)
sz_inches = N.array(im.shape[:2])/dpi

fig = plt.figure(figsize=sz_inches[::-1])

ax = fig.add_axes([0,0,1,1], frameon=False)
ax.imshow(im)
ax.set_axis_off()

# data = np.random.randint(0, 100, (256, 256))
# save_image(data, '1.png')

with fiona.open(infile, 'r', driver="GeoJSON") as source:
    for rec in source:
        g = shape(rec['geometry'])
        coords = N.vstack([N.array(p.coords) for p in g.geoms])
        type = rec['properties']['type']
        if type not in colors:
            continue

        ax.plot(coords[:,0], -coords[:,1], color=colors[type], linewidth=8)

fig.savefig(outfile, dpi=dpi)

