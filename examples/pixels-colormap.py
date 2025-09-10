# Package: Graphic Server Protocol
# Authors: Nicolas P .Rougier <nicolas.rougier@gmail.com>
# License: BSD 3 clause
"""
Pixels visual (colormap)
=======================

This example shows the Pixels visual where pixels are colored according to screen coordinates (x,y) and depth (z) using a colormap.
"""
# Experiment to handle intellisense in VSCode
from gsp.matplotlib import core, visual, glm
from gsp import transform
import matplotlib.pyplot as plt
import numpy as np

import gsp
gsp.use("matplotlib")

canvas = core.Canvas(512, 512, 100.0)
viewport = core.Viewport(canvas, 0, 0, 512, 512, [1,1,1,1])
colormap = transform.Colormap("magma")
depth = transform.Out("screen[positions].z")
point_count = 150_000
positions_3d = glm.as_vec3(np.random.uniform(-1, +1, (point_count,3)))
point_colormap = colormap(depth)
pixels = visual.Pixels(positions=positions_3d, colors=point_colormap)

# Set up gsp.logging
import logging
gsp.log.setLevel(logging.INFO)

from common.camera import Camera
camera = Camera("perspective", theta=50, phi=50, log_fps_enabled=True)
camera.connect(viewport, "motion",  pixels.render)
camera.save("output/pixels-colormap.png")
camera.run()
