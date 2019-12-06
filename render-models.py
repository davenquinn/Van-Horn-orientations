# Script save model renders for selected cameras (or all aligned cameras if no aligned cameras selected)
# to the same folder where the source photos are present with the "_render" suffix.
#
# This is python script for Metashape Pro. Scripts repository: https://github.com/agisoft-llc/metashape-scripts

import Metashape
import os
import sys

camera_labels = sys.argv[1:]

def get_cameras(chunk):
    return [camera
            for camera in chunk.cameras
            if camera.transform
            and camera.type == Metashape.Camera.Type.Regular]


def render_cameras():
    app = Metashape.app
    doc = Metashape.Document()

    doc.open(os.getenv('METASHAPE_MODEL'))
    chunk = doc.chunk

    if not chunk.model:
        raise Exception("No model!")

    cameras = [c for chunk.cameras if c.label in camera_labels]
    if len(cameras) == 0:
        cameras = get_cameras(chunk)

    for camera in cameras:
        render = chunk.model.renderImage(camera.transform, camera.sensor.calibration)
        photo_dir = os.path.dirname(camera.photo.path)
        photo_filename = os.path.basename(camera.photo.path)
        render_filename = os.path.splitext(photo_filename)[0] + "_render.jpg"
        print(render_filename)
        render.save(os.path.join("renders", render_filename))

render_cameras()
