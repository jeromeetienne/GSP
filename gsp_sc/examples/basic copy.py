"""
Basic example of creating and rendering a simple GSP scene with matplotlib.
"""

import numpy as np
import os
import gsp_sc.src as gsp_sc

# Create a GSP scene
canvas = gsp_sc.core.Canvas(512, 512, 100)
viewport = gsp_sc.core.Viewport(0, 0, canvas.width, canvas.height, gsp_sc.Constants.White)
canvas.add(viewport)

# Add some random points
n_points = 100
positions_np = np.random.uniform(-0.5, 0.5, (n_points, 3)).astype(np.float64)
sizes_np = np.random.uniform(5, 10, n_points).astype(np.float32)
pixels = gsp_sc.visuals.Pixels(positions_np, sizes_np, gsp_sc.Constants.Green)
viewport.add(pixels)

# Render the scene with matplotlib
camera = gsp_sc.core.Camera("perspective")
renderer = gsp_sc.renderer.matplotlib.MatplotlibRenderer()
image_png_buffer = renderer.render(canvas, camera, True)

# Save the rendered image to a file
__dirname__ = os.path.dirname(os.path.abspath(__file__))
image_path = f"{__dirname__}/output/{os.path.basename(__file__).replace('.py', '')}.png"
with open(image_path, "wb") as png_file:
    png_file.write(image_png_buffer)
print(f"Rendered image saved to {image_path}")
