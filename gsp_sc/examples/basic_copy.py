"""
Basic example of creating and rendering a simple GSP scene with matplotlib.
"""

import numpy as np
from gsp_sc.src.core.canvas import Canvas
from gsp_sc.src.core.viewport import Viewport
from gsp_sc.src.core.camera import Camera
from gsp_sc.src.renderer.matplotlib import MatplotlibRenderer
from gsp_sc.src.visuals.pixels import Pixels

# Create a GSP scene
canvas = Canvas(512, 512, 100)
viewport = Viewport(0, 0, canvas.width, canvas.height, (1,1,1,1))
canvas.add(viewport)

# Add some random points
n_points = 100
positions = np.random.uniform(-0.5, 0.5, (n_points, 3)).astype(np.float64)
pixels = Pixels(positions)
viewport.add(pixels)

# Render the scene with matplotlib
camera = Camera("perspective")
renderer = MatplotlibRenderer()
renderer.render(canvas, camera, True)
