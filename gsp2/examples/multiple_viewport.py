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

viewport1 = gsp2.core.Viewport(0, 0, 256, 256, (1, 1, 1, 1))
canvas.add_viewport(viewport=viewport1)

viewport2 = gsp2.core.Viewport(256, 0, 256, 256, (1, 1, 1, 1))
canvas.add_viewport(viewport=viewport2)

# Add some random points
n_points = 100
positions_np = np.random.uniform(-0.5, 0.5, (n_points, 2)).astype(np.float32)
sizes_np = np.random.uniform(5, 10, n_points).astype(np.float32)
pixels = gsp2.visuals.Pixels(positions=positions_np, sizes=sizes_np, colors=(0, 1, 0, 0.5))
viewport1.add_visual(pixels)
viewport2.add_visual(pixels)

# Add an image
image_path = f"{__dirname__}/../../examples/images/UV_Grid_Sm.jpg"
image_data_np = mpl_img.imread(image_path)
image = gsp2.visuals.Image(bounds=(-1, +1, -1, +1), image_data=image_data_np)
viewport1.add_visual(image)

# Render the scene
# rendered_image_path = f"{__dirname__}/output/rendered_image.png"
matplotlib_renderer = gsp2.renderer.matplotlib.MatplotlibRenderer()
# matplotlib_renderer.render(canvas)



# Export the scene to JSON
json_renderer = gsp2.renderer.json.JsonRenderer()
scene_json = json_renderer.render(canvas)

json_output_path = f"{__dirname__}/output/scene.json"
with open(json_output_path, 'w') as json_file:
    json_file.write(scene_json)


# Load the scene from JSON
with open(json_output_path, 'r') as json_file:
    scene_json_loaded = json_file.read()

json_parser = gsp2.renderer.json.JsonParser()
canvas_loaded = json_parser.parse(scene_json_loaded)

rendered_image_loaded_path = f"{__dirname__}/output/rendered_image_loaded.png"
matplotlib_renderer.render(canvas_loaded, image_filename=rendered_image_loaded_path)