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
from matplotlib import patches
from plot_colors import colors

def plot_pole(ax, o, *args, **kwargs):
    sdr = o.strike_dip_rake()
    uncertain_pole(ax,
        *sdr,
        *o.angular_errors(),
        *args, **kwargs)

infiles = sys.argv[1:-1]
file_out = sys.argv[-1]

fig = plt.figure()

ax = fig.add_subplot(111, projection="polar")
ax.set_theta_zero_location('N')
ax.set_theta_direction(-1)
ax.set_rlim([0,60])
ax.grid()

for file_in in infiles:
    with fiona.open(file_in,'r', driver="GeoJSON") as source:
        for rec in source:
            g = shape(rec['geometry'])
            coords = N.vstack([N.array(p.coords) for p in g.geoms])
            orient = Orientation(coords)
            type = rec['properties']['type']
            if type not in colors:
                continue

            zorder = 10 if type == "interlamination" else 5

            mx = N.radians(orient.angular_errors()[1])
            opacity = 1-mx**0.5
            if opacity < 0.1:
                opacity = 0.1

            plot_pole(ax, orient,
                    alpha=opacity, color=colors[type], zorder=zorder)

fig.legend(handles=[
    patches.Patch(color=colors['interlamination'], label='Bedding'),
    patches.Patch(color=colors['cross-lamination'], label='Cross-bedding')
], frameon=False)

ax.grid()

#ax.set_rticks([15,30,45,60])
#ax.grid(zorder=12)
#ax.set_axisbelow(False)

fig.savefig(file_out, bbox_inches='tight')

