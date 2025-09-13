import gsp_sc.src as gsp_sc
import numpy as np

import os
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

# Add some random points
n_points = 1000
positions_np = np.random.uniform(-0.5, 0.5, (n_points, 2)).astype(np.float32)
sizes_np = np.random.uniform(5, 10, n_points).astype(np.float32)
pixels = gsp_sc.visuals.Pixels(
    positions=positions_np, sizes=sizes_np, colors=gsp_sc.Constants.Green
)
viewport.add(pixels)

###############################################################################
# Render the scene using a network renderer
#
network_renderer = gsp_sc.renderer.network.NetworkRenderer(
    server_url="http://localhost:5000/"
)
image_png_data = network_renderer.render(canvas)

###############################################################################
# Save the image to a file
#
image_path = f"{__dirname__}/output/network_rendered_image.png"
with open(image_path, "wb") as f:
    f.write(image_png_data)
print(f"Image saved to {image_path}")
