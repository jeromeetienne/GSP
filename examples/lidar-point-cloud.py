"""
from datoviz library - https://datoviz.org/gallery/showcase/lidar/
"""

import os

# Experiment to handle intellisense in VSCode
from gsp.matplotlib import core, visual, glm
import matplotlib.pyplot as plt
import numpy as np

import gsp
gsp.use("matplotlib")

import libs.point_cloud_lib as point_cloud_lib
import libs.point_cloud_display as point_cloud_display

# Set up gsp.logging
import logging
gsp.log.setLevel(logging.INFO)

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


# Load the LIDAR data
point_cloud_npz_filename = f'{os.path.dirname(__file__)}/data/lidar.npz'
point_positions, point_colors = point_cloud_lib.load_npz_point_cloud(point_cloud_npz_filename)
print(f'Loaded LIDAR data with {len(point_positions)} points.')
gsp.log.warning(f'Loaded LIDAR data with {len(point_positions)} points.')

#
# Crop geometry
#
point_positions, point_colors = point_cloud_lib.geometry_crop(point_positions=point_positions, point_colors=point_colors,
                    x_min=-0.2, x_max=0.2,
                    z_min=-0.2, z_max=0.2,)

print(f'Loaded LIDAR data with {len(point_positions)} points.')

#
# DOWNSAMPLING
#

point_positions, point_colors = point_cloud_lib.downsample(
    point_positions=point_positions,
    point_colors=point_colors,
    # wished_point_count=5_000_000
    wished_point_count=400_000
    # wished_point_count=50_000
)

print(f'Downsampling - Keeping {len(point_positions)} points after downsampling.')

# Display geometry information
point_cloud_lib.print_geometry_info(point_positions)


point_cloud_display.display_gsp(point_positions, point_colors)

