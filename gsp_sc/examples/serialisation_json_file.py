import gsp_sc.src as gsp_sc
import numpy as np
import matplotlib.image as mpl_img


import os
__dirname__ = os.path.dirname(os.path.abspath(__file__))

canvas = gsp_sc.core.Canvas(width=512, height=512, dpi=100)

###############################################################################
# Create a viewport
#
viewport = gsp_sc.core.Viewport(0, 0, 256, 256, (1, 1, 1, 1))
canvas.add(viewport=viewport)

###############################################################################
# Add some random points to both viewports
#
n_points = 100
positions_np = np.random.uniform(-0.5, 0.5, (n_points, 3)).astype(np.float32)
sizes_np = np.random.uniform(5, 10, n_points).astype(np.float32)
pixels = gsp_sc.visuals.Pixels(positions=positions_np, sizes=sizes_np, colors=(0, 1, 0, 0.5))
viewport.add(pixels)

###############################################################################
# Export the scene to JSON and save to file
#
json_renderer = gsp_sc.renderer.json.JsonRenderer()
scene_json = json_renderer.render(canvas)

json_output_path = f"{__dirname__}/output/scene.json"
with open(json_output_path, 'w') as json_file:
    json_file.write(scene_json)

print(f"Scene exported to JSON and saved to {json_output_path}")