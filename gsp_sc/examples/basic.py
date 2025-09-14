import matplotlib
import matplotlib.pyplot
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

###############################################################################
# Add some random points
#
n_points = 100
positions_np = np.random.uniform(-0.5, 0.5, (n_points, 3)).astype(np.float64)
sizes_np = np.random.uniform(5, 10, n_points).astype(np.float32)
pixels = gsp_sc.visuals.Pixels(
    positions=positions_np, sizes=sizes_np, colors=gsp_sc.Constants.Green
)
viewport.add(pixels)

###############################################################################
# Add a mesh
#
obj_mesh_path = f"{__dirname__}/data/bunny.obj"
mesh = gsp_sc.visuals.Mesh.from_obj_file(
    obj_mesh_path,
    cmap=matplotlib.pyplot.get_cmap("magma"),
    edgecolors=(0, 0, 0, 0.25),
)
viewport.add(mesh)

###############################################################################
# Render the scene with matplotlib
#
camera = gsp_sc.core.Camera(camera_type="perspective")
renderer = gsp_sc.renderer.matplotlib.MatplotlibRenderer()
image_png_buffer = renderer.render(canvas, camera, interactive=True)

# Save the rendered image to a file
image_path = f"{__dirname__}/output/basic.png"
with open(image_path, "wb") as png_file:
    png_file.write(image_png_buffer)
print(f"Rendered image saved to {image_path}")
