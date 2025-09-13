import gsp_sc.src as gsp_sc
import numpy as np
import matplotlib.image as mpl_img


import os
__dirname__ = os.path.dirname(os.path.abspath(__file__))


canvas = gsp_sc.core.Canvas(width=512, height=512, dpi=100)

###############################################################################
# Create two viewports
viewport1 = gsp_sc.core.Viewport(0, 0, 256, 256, (1, 1, 1, 1))
canvas.add(viewport1)

viewport2 = gsp_sc.core.Viewport(256, 0, 256, 256, (1, 1, 1, 1))
canvas.add(viewport2)

###############################################################################
# Add some random points to viewport1 and viewport2
#
n_points = 100
positions_np = np.random.uniform(-0.5, 0.5, (n_points, 2)).astype(np.float32)
sizes_np = np.random.uniform(5, 10, n_points).astype(np.float32)
pixels = gsp_sc.visuals.Pixels(positions=positions_np, sizes=sizes_np, colors=(0, 1, 0, 0.5))
viewport1.add(pixels)
viewport2.add(pixels)

###############################################################################
# Add an image to viewport1
#
image_path = f"{__dirname__}/../../examples/images/UV_Grid_Sm.jpg"
image_data_np = mpl_img.imread(image_path)
image = gsp_sc.visuals.Image(bounds=(-1, +1, -1, +1), image_data=image_data_np)
viewport1.add(image)

###############################################################################
# Render the scene
#
matplotlib_renderer = gsp_sc.renderer.matplotlib.MatplotlibRenderer()
matplotlib_renderer.render(canvas)
