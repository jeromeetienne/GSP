"""
from datoviz library - https://datoviz.org/gallery/showcase/lidar/
"""

import os

# Experiment to handle intellisense in VSCode
from gsp.matplotlib import core, visual, glm
import matplotlib.pyplot as plt
import numpy as np

# Set up logging
from gsp import log
import logging
log.setLevel(logging.INFO)

import gsp
gsp.use("matplotlib")

import libs.point_cloud_lib as point_cloud_lib


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
point_cloud_npz_filename = os.path.join(__dirname__, 'data/lidar.npz')
    
# Load the LIDAR data
point_positions, point_colors = point_cloud_lib.load_lidar(point_cloud_npz_filename)
print(f'Loaded LIDAR data with {len(point_positions)} points.')
log.warning(f'Loaded LIDAR data with {len(point_positions)} points.')

# Measure size of the point cloud
x_max, x_min = point_positions[:, 0].max(), point_positions[:, 0].min()
y_max, y_min = point_positions[:, 1].max(), point_positions[:, 1].min()
z_max, z_min = point_positions[:, 2].max(), point_positions[:, 2].min()
print(f'Point cloud size: x: {x_max - x_min}, y: {y_max - y_min}, z: {z_max - z_min}')
print(f'Point cloud size: {len(point_positions)} points')



# x_min = -0.2
# x_max = 0.2
# z_min = -0.2
# z_max = 0.2


# # Keep only points that are within a certain range
# mask = (point_positions[:, 0] > x_min) & (point_positions[:, 0] < x_max) & \
#        (point_positions[:, 1] > y_min) & (point_positions[:, 1] < y_max) & \
#        (point_positions[:, 2] > z_min) & (point_positions[:, 2] < z_max)
# point_positions = point_positions[mask]
# point_colors = point_colors[mask]


point_positions, point_colors = point_cloud_lib.geometry_crop(point_positions=point_positions, point_colors=point_colors,
                    x_min=-0.2, x_max=0.2,
                    z_min=-0.2, z_max=0.2,)

print(f'Loaded LIDAR data with {len(point_positions)} points.')
point_count = point_positions.shape[0]


#
# DOWNSAMPLING
#

# Compute the downsampling factor
point_count_max = 5_000_000
# point_count_max = 400_000
# point_count_max = 50_000
# point_count_max = point_count


# Downsample by randomly selecting points 
point_keep_factor = point_count // point_count_max

# Sanity check - always keep at least 1 point
if point_keep_factor < 1:
    point_keep_factor = 1
    print(f'Point count is already below {point_count_max}, no downsampling needed.')
point_indices = np.random.choice(point_count, point_count // point_keep_factor, replace=False)

# recompute positions and colors after downsampling
point_positions = point_positions[point_indices]
point_colors = point_colors[point_indices]

print(f'Downsampling - Keeping {len(point_positions)} points after downsampling.')


# Scale positions for better visualization
geometry_scale_factor = 5.0
point_positions *= geometry_scale_factor

# Display in pixels
pixels = visual.Pixels(point_positions, colors=gsp.grey)
# pixels = visual.Pixels(point_positions, colors=point_colors)

#
# display in points
# sizes = glm.float(len(point_positions))
# sizes[...] = 3
# pixels = visual.Points(point_positions, sizes, gsp.grey, gsp.black, [0])
# pixels = visual.Points(point_positions, sizes, point_colors, gsp.black, [0])


canvas = core.Canvas(1024, 1024, 100.0)
viewport = core.Viewport(canvas, 0, 0, 1024, 1024, [1,1,1,1])


print('Rendering pixels visual...')

# measure_fps()

from libs.camera import Camera
camera = Camera("perspective", theta=-30, phi=0)
camera.connect(viewport, "motion",  pixels.render)
# camera.connect(viewport, "scroll",  pixels.render)
# camera.save("output/pixels-3d.png")
camera.run()
