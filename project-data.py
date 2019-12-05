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

import Metashape
import time
import sys
import fiona
from json import load, dump
from os import path, environ
from shapely.geometry import mapping, shape
from shapely.ops import transform

__dirname__ = path.dirname(__file__)
__start__ = time.time()

# Add local modules to path
sys.path.append(path.join(__dirname__,'modules'))

def cross(a, b):
    result = Metashape.Vector([a.y*b.z - a.z*b.y, a.z*b.x - a.x*b.z, a.x*b.y - a.y *b.x])
    return result

def geometry_transformer(fn):
    """
    Creates a transformation function for a geometry,
    given a function that operates on points.
    """

    # Create processors for various levels of coordinate nesting
    _array = lambda c: [fn(i) for i in c]
    _multi = lambda c: [_array(i) for i in c]
    _collection = lambda c: [_multi(i) for i in c]

    processors = {
        'Point': fn,
        'LineString': _array,
        'Polygon': _multi,
        'MultiPoint': _array,
        'MultiLineString':_multi,
        'MultiPolygon': _collection
    }
    def processor(geom):
        _ = processors[geom['type']]
        geom['coordinates'] = _(geom['coordinates'])
        return geom
    return processor

# try:
#     script_name, file_in = argv
# except ValueError:
#     print("Need to specify input file")

file_in = sys.argv[1]
file_out = sys.argv[2]

app = Metashape.app
doc = Metashape.Document()

doc.open(environ.get("METASHAPE_MODEL"))
chunk = doc.chunk
model = chunk.model

# Build a directory of cameras in the active chunk
cameras = {path.splitext(c.label)[0]: c for c in chunk.cameras}

# create a point function based on image ids
def point_function(x,y,z=None):
    """
    Transform individual point to 3d coordinates
    """
    image_id = "DJI_0062"
    camera = cameras[image_id]
    # Presumes image position from top left
    # Sometimes negative Y coordinates are implicit
    y = abs(y)

    point_2D = camera.unproject(Metashape.Vector((x,y)))
    vect = model.pickPoint(camera.center, point_2D)

    #estimating ray and surface intersection
    return tuple(vect)

with fiona.open(file_in,'r', driver="GeoJSON") as source:
    with fiona.open(file_out,'w',driver=source.driver, schema=source.schema) as sink:
        for rec in source:
            geom = shape(rec['geometry'])
            geom2 = transform(point_function, geom)
            rec['geometry'] = mapping(geom2)
            sink.write(rec)

__end__ = time.time()-__start__
print(f"--- {__end__} seconds ---")

