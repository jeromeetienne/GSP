import gsp2.src as gsp2
import numpy as np
import matplotlib.image as mpl_img


import os
__dirname__ = os.path.dirname(os.path.abspath(__file__))


# TODO
# - multiple viewports
# - from/to file
# - how to implement 3d....

canvas = gsp2.core.Canvas(width=512, height=512, dpi=100)

viewport = gsp2.core.Viewport(0, 0, 256, 256, gsp2.core.Color(1, 1, 1, 1))
canvas.add_viewport(viewport=viewport)

# Add some random points
n_points = 1000
positions_np = np.random.uniform(-0.5, 0.5, (n_points, 2)).astype(np.float32)
sizes_np = np.random.uniform(0, 100, n_points).astype(np.float32)
pixels = gsp2.visuals.Pixels(positions=positions_np, sizes=sizes_np, colors=(0, 1, 0, 0.5))
viewport.add_visual(pixels)

# Add an image
image_path = f"{__dirname__}/../../examples/images/UV_Grid_Sm.jpg"
image_data_np = mpl_img.imread(image_path)
image = gsp2.visuals.Image(bounds=(0, 0.5, 0, 0.5), image_data=image_data_np)
viewport.add_visual(image)



rendered_image_path = f"{__dirname__}/output/rendered_image.png"
renderer = gsp2.renderer.matplotlib.MatplotlibRenderer()
renderer.render(canvas)
