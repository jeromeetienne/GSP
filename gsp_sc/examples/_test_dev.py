import matplotlib.pyplot
import gsp_sc.src as gsp_sc
import numpy as np
import matplotlib.image


import os
__dirname__ = os.path.dirname(os.path.abspath(__file__))


canvas = gsp_sc.core.Canvas(width=512, height=512, dpi=100)

###############################################################################
# Create two viewports
viewport1 = gsp_sc.core.Viewport(0, 0, 256, 256, (1, 1, 1, 1))
canvas.add(viewport1)

viewport2 = gsp_sc.core.Viewport(256, 0, 256, 256, (1, 1, 1, 1))
canvas.add(viewport2)

viewport3 = gsp_sc.core.Viewport(0, 256, 256, 256, (1, 1, 1, 1))
canvas.add(viewport3)

###############################################################################
# Add some random points to viewport1 and viewport2
#
n_points = 100
positions_np = np.random.uniform(-0.5, 0.5, (n_points, 3)).astype(np.float32)
sizes_np = np.random.uniform(5, 10, n_points).astype(np.float32)
pixels = gsp_sc.visuals.Pixels(positions=positions_np, sizes=sizes_np, colors=(0, 1, 0, 0.5))
viewport1.add(pixels)
viewport2.add(pixels)

###############################################################################
# Add a mesh
#
obj_mesh_path = f"{__dirname__}/data/bunny.obj"
mesh = gsp_sc.visuals.Mesh.from_obj_file(
    obj_mesh_path,
    cmap=matplotlib.pyplot.get_cmap("magma"),
    edgecolors=(0, 0, 0, 0.25), # type: ignore
)
viewport2.add(mesh)
viewport3.add(mesh)

###############################################################################
# Render the scene
#
camera = gsp_sc.core.Camera(camera_type="perspective")
matplotlib_renderer = gsp_sc.renderer.matplotlib.MatplotlibRenderer()
image_png_buffer = matplotlib_renderer.render(canvas, camera, show_image=True)

# Save the rendered image to a file
image_path = f"{__dirname__}/output/viewport_multiple.png"
with open(image_path, "wb") as png_file:
    png_file.write(image_png_buffer)
print(f"Rendered image saved to {image_path}")