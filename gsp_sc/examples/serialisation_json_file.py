"""
Example of serialising a scene to JSON and MessagePack files.
"""

import gsp_sc.src as gsp_sc
import numpy as np
import matplotlib.pyplot
import msgpack


import os
__dirname__ = os.path.dirname(os.path.abspath(__file__))

canvas = gsp_sc.core.Canvas(width=512, height=512, dpi=100)

###############################################################################
# Create a viewport
#
viewport = gsp_sc.core.Viewport(0, 0, 256, 256, (1, 1, 1, 1))
canvas.add(viewport=viewport)

###############################################################################
# Add some random points to viewport
#
n_points = 1000
positions_np = np.random.uniform(-0.5, 0.5, (n_points, 3)).astype(np.float32)
sizes_np = np.random.uniform(5, 10, n_points).astype(np.float32)
pixels = gsp_sc.visuals.Pixels(positions=positions_np, sizes=sizes_np, colors=(0, 1, 0, 0.5))
viewport.add(pixels)

###############################################################################
# Add a mesh
#
obj_mesh_path = f"{__dirname__}/data/bunny.obj"
mesh = gsp_sc.visuals.Mesh.from_obj_file(
    obj_mesh_path,
    cmap=matplotlib.pyplot.get_cmap("magma"),
    edgecolors=(0, 0, 0, 0.25), # type: ignore
)
viewport.add(mesh)

###############################################################################
# Render the scene to JSON and save to file
#
camera = gsp_sc.core.Camera("perspective")
json_renderer = gsp_sc.renderer.json.JsonRenderer()
scene_json = json_renderer.render(canvas, camera)

# save to file as json
json_output_path = f"{__dirname__}/output/{os.path.basename(__file__)}_scene.json"
with open(json_output_path, 'w') as msgpack_file:
    msgpack_file.write(scene_json)

print(f"Scene exported to JSON and saved to {json_output_path}. length={len(scene_json)}")

###############################################################################
# Save as messagepack too
#

import json
scene_json_obj = json.loads(scene_json)
msgpack_output_path = f"{__dirname__}/output/{os.path.basename(__file__)}_scene.msgpack"
scene_msgpack = msgpack.packb(scene_json_obj, use_bin_type=True)
with open(msgpack_output_path, 'wb') as msgpack_file:
    msgpack_file.write(scene_msgpack)

print(f"Scene exported to MessagePack and saved to {msgpack_output_path}. length={len(scene_msgpack)}")

