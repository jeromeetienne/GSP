# Package: Graphic Server Protocol / Matplotlib
# Authors: Nicolas P .Rougier <nicolas.rougier@gmail.com>
# License: BSD 3 clause
"""
From https://datoviz.org/gallery/visuals/volume/
"""
# Experiment to handle intellisense in VSCode
from gsp.matplotlib import core, visual, glm
import matplotlib.pyplot as plt
import numpy as np
import libs.asset_downloader as asset_downloader

import gsp

gsp.use("matplotlib")


############################

import libs.asset_downloader as asset_downloader
import gzip

volume_path = asset_downloader.download_data("volumes/allen_mouse_brain_rgba.npy.gz")
print(f"Loaded point cloud data from {volume_path}")
with gzip.open(volume_path, "rb") as f:
    # volume_data is a (depth, height, width, 4) array where 4 is the RGBA color channels
    volume_data = np.load(f, allow_pickle=True)

# Normalize volume_data colors from [0, 255] to [0, 1]
volume_data = volume_data / 255.0


############################



volume_depth, volume_height, volume_width, color_ndim = volume_data.shape

import time
build_array_time_start = time.perf_counter()

# Create a grid of coordinates
coordinate_z, coordinate_y, coordinate_x = np.meshgrid(
    np.arange(volume_depth),
    np.arange(volume_height),
    np.arange(volume_width),
    indexing="ij"  # ensures (z,y,x) ordering
)

# Normalize coordinates to [-1, 1]
coordinate_z = (coordinate_z / (volume_depth - 1)) * 2 - 1
coordinate_y = (coordinate_y / (volume_height - 1)) * 2 - 1
coordinate_x = (coordinate_x / (volume_width - 1)) * 2 - 1


# Stack into (N, 3) array of positions
positions = np.stack([coordinate_x.ravel(), coordinate_y.ravel(), coordinate_z.ravel()], axis=-1).reshape(-1, 3)
fill_colors = volume_data.reshape(-1, 4)  # rgba per point


build_array_time_end = time.perf_counter()
print(f"Build array time: {build_array_time_end - build_array_time_start:.4f} seconds")

# # Print range of positions
# print(f"Position range: {positions.min()} - {positions.max()}")

# # Print range of fill_colors
# print(f"Fill color range: {fill_colors.min()} - {fill_colors.max()}")

############

# keep only 1% of positions/fill_colors
downsample_factor = 0.0005
point_to_keep = int(downsample_factor * len(positions))
indices = np.random.choice(len(positions), size=point_to_keep, replace=False)
positions = positions[indices]
fill_colors = fill_colors[indices]

###########

# multiply alpha (the forth dimension) of fill_colors by the corresponding volume_data values
alpha_factor = 2
fill_colors[..., 3] *= alpha_factor

# count how many fill_colors got a alpha value > 0
alpha_count = np.sum(fill_colors[..., 3] > 0)
print(f"Alpha count: {alpha_count} len: {len(fill_colors)}")

# optimisation: remove all positions and fill_colors where alpha is 0. it would be invisible anyways
positions = positions[fill_colors[..., 3] > 0]
fill_colors = fill_colors[fill_colors[..., 3] > 0]

# Fake way to remove moire patterns
# positions += 0.003 * np.random.normal(0, 1, positions.shape)

canvas = core.Canvas(width=512, height=512, dpi=100.0)
viewport = core.Viewport(canvas=canvas, x=0, y=0, width=512, height=512, color=gsp.black)

points = visual.Points(
    positions=positions,
    sizes=120.0,
    fill_colors=fill_colors,
    line_colors=[1, 1, 1, 0.1],
    line_widths=[0.0],
)

####

# TODO make a function which change the opacity of the points based on the Z


import logging
gsp.log.setLevel(logging.INFO)

from libs.camera import Camera
camera = Camera("perspective", theta=0, phi=0, log_fps_enabled=True)
camera.connect(viewport, "motion", points.render)
camera.run()
