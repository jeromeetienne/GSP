import gsp2.src as gsp2
import numpy as np
import matplotlib.image as mpl_img


import os

__dirname__ = os.path.dirname(os.path.abspath(__file__))

# TODO
# - multiple viewports
# - from/to file
# - how to implement 3d....
#   - matrix rotation/translation
#   - camera

canvas = gsp2.core.Canvas(width=512, height=512, dpi=100)
viewport = gsp2.core.Viewport(
    origin_x=0,
    origin_y=0,
    width=canvas.width,
    height=canvas.height,
    background_color=gsp2.Constants.White,
)
canvas.add(viewport=viewport)

# Add some random points
n_points = 100
positions_np = np.random.uniform(-0.5, 0.5, (n_points, 2)).astype(np.float32)
sizes_np = np.random.uniform(5, 10, n_points).astype(np.float32)
pixels = gsp2.visuals.Pixels(
    positions=positions_np, sizes=sizes_np, colors=gsp2.Constants.Green
)
viewport.add(pixels)

# Render the scene
renderer = gsp2.renderer.matplotlib.MatplotlibRenderer()
renderer.render(canvas)
