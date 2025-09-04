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
    volume_data = np.load(f, allow_pickle=True)

############################

volume_depth, volume_height, volume_width, _ = volume_data.shape

volume_downsample = 0.05


canvas = core.Canvas(width=1024, height=1024, dpi=500.0)
viewport = core.Viewport(canvas=canvas, x=0, y=0, width=1024, height=1024, color=gsp.black)


len_x = int(volume_width * volume_downsample)
len_y = int(volume_height * volume_downsample)
len_z = int(volume_depth * volume_downsample)


point_count = len_x * len_y * len_z
 
# TODO should i sample that randomly - would be easier to vectorize
positions = glm.vec3(point_count)
fill_colors = glm.vec4(point_count)

# positions[...] = np.random.uniform(-1, +1, (n, 3))
# setup positions array to be a dense cube
linspace_x = np.linspace(-1, 1, len_x)
linspace_y = np.linspace(-1, 1, len_y)
linspace_z = np.linspace(-1, 1, len_z)

# TODO should be vectorized
for index_x in range(len_x):
    for index_y in range(len_y):
        for index_z in range(len_z):
            array_index = index_x * len_y * len_z + index_y * len_z + index_z
            positions[array_index] = [ linspace_z[index_z], linspace_y[index_y], linspace_x[index_x]]
            fill_colors[array_index] = volume_data[
                int(index_z / volume_downsample),
                int(index_y / volume_downsample),
                int(index_x / volume_downsample),
            ]


# Normalize fill_colors from [0, 255] to [0, 1]
fill_colors = fill_colors / 255.0

# multiply alpha (the forth dimension) of fill_colors by the corresponding volume_data values
fill_colors[..., 3] *= 1

# count how many fill_colors got a alpha value > 0
alpha_count = np.sum(fill_colors[..., 3] > 0)
print(f"Alpha count: {alpha_count} len: {len(fill_colors)}")

# optimisation: remove all positions and fill_colors where alpha is 0. it would be invisible anyways
positions = positions[fill_colors[..., 3] > 0]
fill_colors = fill_colors[fill_colors[..., 3] > 0]

# Fake way to remove moire patterns
positions += 0.003 * np.random.normal(0, 1, positions.shape)

points = visual.Points(
    positions=positions,
    sizes=80.0,
    fill_colors=fill_colors,
    line_colors=[1, 1, 1, 0.1],
    line_widths=[0.0],
)


####

# TODO make a function which change the opacity of the points based on the Z

from libs.camera import Camera

camera = Camera("perspective", theta=0, phi=0)
camera.connect(viewport, "motion", points.render)
camera.run()
