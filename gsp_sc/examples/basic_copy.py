"""
Basic example of creating and rendering a simple GSP scene with matplotlib.
"""

import numpy as np
from gsp_sc.src.core.canvas import Canvas
from gsp_sc.src.core.viewport import Viewport
from gsp_sc.src.core.camera import Camera
from gsp_sc.src.renderer.matplotlib import MatplotlibRenderer
from gsp_sc.src.renderer.json import JsonRenderer
from gsp_sc.src.renderer.network import NetworkRenderer
from gsp_sc.src.visuals.pixels import Pixels

# Create a GSP scene
canvas = Canvas(512, 512, 100)
viewport = Viewport(0, 0, canvas.width, canvas.height, (1,1,1,1))
canvas.add(viewport)

# Add some random points
n_points = 100
positions = np.random.uniform(-0.5, 0.5, (n_points, 3))
pixels = Pixels(positions)
viewport.add(pixels)

# Render the scene with matplotlib
camera = Camera("perspective")
renderer = MatplotlibRenderer()
png_image = renderer.render(canvas, camera)

# Export the scene to JSON
json_renderer = JsonRenderer()
scene_json = json_renderer.render(canvas, camera)

# Render the scene remotely (if you have a GSP server running)
network_renderer = NetworkRenderer("http://localhost:5000")
png_image2 = network_renderer.render(canvas, camera)