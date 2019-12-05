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
import fiona
import numpy as N
from os import path, environ
from matplotlib import pyplot as plt
from shapely.geometry import shape
from attitude import Orientation
from attitude.display.polar import pole, pole_error, uncertain_pole

def plot_pole(ax, o, *args, **kwargs):
    sdr = o.strike_dip_rake()
    uncertain_pole(ax,
        *sdr,
        *o.angular_errors(),
        *args, **kwargs)

file_in = sys.argv[1]
file_out = sys.argv[2]

fig = plt.figure()

ax = fig.add_subplot(111, projection="polar")
ax.set_theta_zero_location('N')
ax.set_theta_direction(-1)
ax.set_rlim([0,60])
ax.set_rticks([15,30,45,60])

with fiona.open(file_in,'r', driver="GeoJSON") as source:
    for rec in source:
        g = shape(rec['geometry'])
        coords = N.vstack([N.array(p.coords) for p in g.geoms])
        orient = Orientation(coords)
        type = rec['properties']['type']

        ctype = "seagreen" if type == 'interlamination' else 'skyblue'

        plot_pole(ax, orient, alpha=0.5, color=ctype)


ax.grid()
ax.grid()
fig.legend()

fig.savefig(sys.argv[2], bbox_inches='tight')

