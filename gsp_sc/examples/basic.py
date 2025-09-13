import gsp_sc.src as gsp_sc
import numpy as np
import matplotlib.image as mpl_img

import mpl3d.camera
import mpl3d.glm
import mpl3d.mesh

import os
__dirname__ = os.path.dirname(os.path.abspath(__file__))


canvas = gsp_sc.core.Canvas(width=512, height=512, dpi=100)
viewport = gsp_sc.core.Viewport(
    origin_x=0,
    origin_y=0,
    width=canvas.width,
    height=canvas.height,
    background_color=gsp_sc.Constants.White,
)
canvas.add(viewport=viewport)

# Add some random points
n_points = 100
positions_np = np.random.uniform(-0.5, 0.5, (n_points, 2)).astype(np.float32)
sizes_np = np.random.uniform(5, 10, n_points).astype(np.float32)
pixels = gsp_sc.visuals.Pixels(
    positions=positions_np, sizes=sizes_np, colors=gsp_sc.Constants.Green
)
viewport.add(pixels)

# Render the scene
renderer = gsp_sc.renderer.matplotlib.MatplotlibRenderer()
renderer.render(canvas)
