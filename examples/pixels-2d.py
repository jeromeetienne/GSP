# Package: Graphic Server Protocol
# Authors: Nicolas P .Rougier <nicolas.rougier@gmail.com>
# License: BSD 3 clause
"""
Pixels visual (2D)
==================

This example shows the Pixels visual where pixels are spread randomly
inside a square that can be zoomed using the mouse and an orthographic
camera.
"""

# Experiment to handle intellisense in VSCode
from gsp.matplotlib import core, visual, glm
import matplotlib.pyplot as plt
import numpy as np

import gsp
gsp.use("matplotlib")

canvas = core.Canvas(512, 512, 10.0)
viewport = core.Viewport(canvas, 0, 0, 512, 512, [1,1,1,1])
pixel_count = 10_000
pixel_positions = glm.to_vec3(np.random.uniform(-1, +1, (pixel_count,2)))
sorted_indices = np.argsort(pixel_positions[:, 1])
pixel_positions = pixel_positions[sorted_indices]
pixel_colors = np.zeros((pixel_count, 4), dtype=np.float32)
# pixel_colors[:pixel_count//2] = [0, 0, 0, 1]   # Black, opaque
# pixel_colors[pixel_count//2:] = [1, 1, 1, 1]   # White, opaque
pixel_colors[pixel_positions[:, 1] >= 0] = [0, 0, 0, 1]    # Black, opaque
pixel_colors[pixel_positions[:, 1] < 0] = [0, 0, 1, 1]     # Blue, opaque
pixel_colors = glm.to_vec4(pixel_colors)
pixels = visual.Pixels(pixel_positions, colors=pixel_colors)




from common.camera import Camera
camera = Camera("ortho", log_fps_enabled=True)
camera.connect(viewport, "motion",  pixels.render)
# camera.save("output/pixels-2d.png")
camera.run()
