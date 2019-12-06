# Script save model renders for selected cameras (or all aligned cameras if no aligned cameras selected)
# to the same folder where the source photos are present with the "_render" suffix.
#
# This is python script for Metashape Pro. Scripts repository: https://github.com/agisoft-llc/metashape-scripts

import Metashape
import os
import sys

camera_labels = [os.path.basename(i) for i in sys.argv[1:-1]]
output_dir = sys.argv[-1]

def render_cameras():
    app = Metashape.app
    doc = Metashape.Document()

    doc.open(os.getenv('METASHAPE_MODEL'))
    chunk = doc.chunk

    if not chunk.model:
        raise Exception("No model!")

    cameras = [c for c in chunk.cameras if c.label in camera_labels]

    for camera in cameras:
        render = chunk.model.renderImage(camera.transform, camera.sensor.calibration)
        photo_dir = os.path.dirname(camera.photo.path)
        photo_filename = os.path.basename(camera.photo.path)
        render_filename = os.path.splitext(photo_filename)[0] + "_render.jpg"
        print(render_filename)
        render.save(os.path.join(output_dir, render_filename))

render_cameras()
