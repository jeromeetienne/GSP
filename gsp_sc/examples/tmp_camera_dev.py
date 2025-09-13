from time import sleep
import gsp_sc.src as gsp_sc
import numpy as np
import mpl3d.camera

import os
from matplotlib.animation import FuncAnimation
__dirname__ = os.path.dirname(os.path.abspath(__file__))

###############################################################################
# Create a GSP scene
#
canvas = gsp_sc.core.Canvas(width=512, height=512, dpi=100)
viewport = gsp_sc.core.Viewport(
    origin_x=0,
    origin_y=0,
    width=canvas.width,
    height=canvas.height,
    background_color=gsp_sc.Constants.White,
)
canvas.add(viewport=viewport)

###############################################################################
# Add some random points
#
n_points = 1_000
positions_np = np.random.uniform(-0.5, 0.5, (n_points, 3)).astype(np.float32)
sizes_np = np.random.uniform(5, 10, n_points).astype(np.float32)
pixels = gsp_sc.visuals.Pixels(
    positions=positions_np, sizes=sizes_np, colors=gsp_sc.Constants.Green
)
viewport.add(pixels)

###############################################################################
# Add an image to viewport
#
import matplotlib.image
image_path = f"{__dirname__}/../../examples/images/UV_Grid_Sm.jpg"
image_data_np = matplotlib.image.imread(image_path)
image = gsp_sc.visuals.Image(bounds=(-1, +1, -1, +1), image_data=image_data_np)
viewport.add(image)

###############################################################################
# Render the scene with matplotlib
#
# mpl3d_camera = mpl3d.camera.Camera("perspective")

renderer = gsp_sc.renderer.matplotlib.MatplotlibRendererDelta()
# renderer.render(canvas, show_image=False)

###############################################################################
# Set up the camera
#

def camera_update(transform) -> None:
    renderer.render(canvas, transform_matrix=transform, show_image=False)

import matplotlib.pyplot as plt
mpl3d_camera = mpl3d.camera.Camera("perspective")
mpl3d_camera.aperture = 10
renderer.render(canvas, transform_matrix=mpl3d_camera.transform, show_image=False)

figure = plt.gcf()
mpl_axes = figure.get_axes()[0]
mpl3d_camera.connect(mpl_axes, camera_update)

plt.show(block=True)

