# Script save model renders for selected cameras (or all aligned cameras if no aligned cameras selected)
# to the same folder where the source photos are present with the "_render" suffix.
#
# This is python script for Metashape Pro. Scripts repository: https://github.com/agisoft-llc/metashape-scripts

import Metashape
import os

def get_cameras(chunk):
    selected_cameras = [camera
            for camera in chunk.cameras
            if camera.transform
            and camera.selected
            and camera.type == Metashape.Camera.Type.Regular]

    if len(selected_cameras) > 0:
        return selected_cameras
    else:
        return [camera for camera in chunk.cameras if camera.transform and camera.type == Metashape.Camera.Type.Regular]


def render_cameras():
    print("Script started...")

    app = Metashape.app
    doc = Metashape.Document()

    doc.open("/Users/Daven/Projects/Van Horn/3D Models/Van Horn Whaleback/Van Horn whaleback v1.psx")
    chunk = doc.chunk

    if not chunk.model:
        raise Exception("No model!")

    for camera in get_cameras(chunk):
        render = chunk.model.renderImage(camera.transform, camera.sensor.calibration)

        photo_dir = os.path.dirname(camera.photo.path)
        photo_filename = os.path.basename(camera.photo.path)
        render_filename = os.path.splitext(photo_filename)[0] + "_render.jpg"
        print(render_filename)
        import IPython; IPython.embed(); raise

        render.save(os.path.join("renders", render_filename))

    print("Script finished!")

render_cameras()
