# Package: Graphic Server Protocol / Matplotlib
# Authors: Nicolas P .Rougier <nicolas.rougier@gmail.com>
# License: BSD 3 clause
"""
From https://datoviz.org/gallery/visuals/volume/
"""
# Experiment to handle intellisense in VSCode
# from gsp.core.types import Color
from gsp.matplotlib import core, visual, glm
import matplotlib.pyplot as plt
import numpy as np
import common.asset_downloader as asset_downloader

############################
# Download/read the volume data
#
import common.asset_downloader as asset_downloader
import gzip

####################################################
# Download/read the volume data
#

volume_path = asset_downloader.download_data("volumes/allen_mouse_brain_rgba.npy.gz")
print(f"Loaded point cloud data from {volume_path}")
with gzip.open(volume_path, "rb") as f:
    volume_data = np.load(f, allow_pickle=True)

# Normalize volume_data colors from [0, 255] to [0, 1]
volume_data = volume_data / 255.0

####################################################
# Create canvas+viewport for the GSP scene
#
canvas = core.Canvas(width=512, height=512, dpi=250.0)
viewport = core.Viewport(
    canvas=canvas, x=0, y=0, width=512, height=512, color=(0, 0, 0, 1)
)

######################################################
# Create a texture from the volume data
#

texture_3d = core.Texture(volume_data, volume_data.shape)

#####################################################
# Create a volume from the texture
#

bound_x = (-1, 1)
bound_y = (-1, 1)
bound_z = (-1, 1)
volume = visual.Volume(
    texture_3d=texture_3d,
    bounds_3d=(bound_x, bound_y, bound_z),
    downsample_ratio=0.00005,
    jitter_position_factor=0.000,
    point_size=200.0,
)

############################

from common.camera import Camera
camera = Camera("perspective", theta=0, phi=0)
camera.connect(viewport, "motion", volume.render)
camera.run()
