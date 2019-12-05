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
from json import load, dump
from sys import argv
from os import path

__dirname__ = path.dirname(__file__)
__start__ = time.time()

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

file_in = path.join(__dirname__,"test-data","DJI_0263.geojson")
file_out = None

app = Metashape.app
doc = Metashape.Document()

doc.open("/Users/Daven/Projects/Van Horn/3D Models/Van Horn Whaleback/Van Horn whaleback v1.psx")
chunk = doc.chunk
model = chunk.model

#
#file_in = app.getOpenFileName("Choose an input GeoJSON file")
file_out = app.getSaveFileName("Choose a location to write output file")

# Build a directory of cameras in the active chunk
cameras = {path.splitext(c.label)[0]: c for c in chunk.cameras}


def process_features(features):
    print("Starting to process features")

    for feature in features:
        image_id = feature['properties']['image']
        print(image_id)

        try:
            camera = cameras[image_id]
        except KeyError:
            continue

        feature['properties']['camera_center'] = list(camera.center)

        # create a point function based on image ids
        def point_function(coords):
            """
            Transform individual point to 3d coordinates
            """
            x,y = coords
            # Presumes image position from top left
            # Sometimes negative Y coordinates are implicit
            y = abs(y)

            point_2D = (x,y)
            vect = camera.unproject(point_2D)

            #estimating ray and surface intersection
            return list(vect)

        _ = geometry_transformer(point_function)
        feature['geometry'] = _(feature['geometry'])
        # Clean up

        yield feature

with open(file_in,'r') as f:
    data = load(f)
features = data["features"]
data['features'] = list(process_features(data['features']))

if not file_out:
    print(data)
else:
    with open(file_out,'w') as f:
        dump(data,f)

print("--- {0} seconds ---".format(time.time()-__start__))
