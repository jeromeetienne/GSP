"""
from datoviz library - https://datoviz.org/gallery/showcase/lidar/
"""

import numpy as np
import os

# Experiment to handle intellisense in VSCode
from gsp.matplotlib import core, visual, glm
import matplotlib.pyplot as plt
import numpy as np

import gsp
gsp.use("matplotlib")


def measure_fps(render_count=3, log_enabled=True):
    """
        Measure the time taken to render the pixels visual multiple times
        NOTE: this is a first attempt, it doesnt really work... i think

    Args:
        render_count (int): Number of times to render the pixels visual
    """
    import time
    # Measure the time taken to render the pixels visual
    start_time = time.time()
    for _ in range(render_count):
        pixels.render(viewport)
    end_time = time.time()
    total_render_time = end_time - start_time
    render_time_one = render_count / total_render_time
    fps = 1 / render_time_one
    if log_enabled:
        print(f'Rendered {len(point_positions)} points in {total_render_time / render_count:.2f} seconds.')
    return fps

# Get the npz file path
__dirname__ = os.path.dirname(__file__)
point_cloud_filename = os.path.join(__dirname__, 'data/lidar.npz')

# Load the LIDAR data
point_cloud_data = np.load(point_cloud_filename)
point_positions, point_colors = point_cloud_data['pos'], point_cloud_data['color']

# point_colors - divide by 255 to normalize colors
point_colors = point_colors / 255.0

print(f'Loaded LIDAR data with {len(point_positions)} points.')
point_count = point_positions.shape[0]


#
# DOWNSAMPLING
#

# Compute the downsampling factor
# point_count_max = 5_000_000
# point_count_max = 400_000
point_count_max = 200_000
# point_count_max = point_count


# Downsample by randomly selecting points 
point_keep_factor = point_count // point_count_max
point_indices = np.random.choice(point_count, point_count // point_keep_factor, replace=False)

# recompute positions and colors after downsampling
point_positions = point_positions[point_indices]
point_colors = point_colors[point_indices]

print(f'Downsampling - Keeping {len(point_positions)} points after downsampling.')


# Scale positions for better visualization
point_positions *= 2

# pixels = visual.Pixels(point_positions, colors=[1, 0, 0, 1])
# pixels = visual.Pixels(point_positions, colors=point_colors)

sizes = glm.float(len(point_positions))
sizes[...] = 1
# pixels = visual.Points(point_positions, sizes, gsp.grey, gsp.black, [0])
pixels = visual.Points(point_positions, sizes, point_colors, point_colors, [0])


canvas = core.Canvas(512, 512, 100.0)
viewport = core.Viewport(canvas, 0, 0, 512, 512, [1,1,1,1])


print('Rendering pixels visual...')

# measure_fps()

from libs.camera import Camera
camera = Camera("perspective", theta=-30, phi=0)
camera.connect(viewport, "motion",  pixels.render)
# camera.connect(viewport, "scroll",  pixels.render)
# camera.save("output/pixels-3d.png")
camera.run()
