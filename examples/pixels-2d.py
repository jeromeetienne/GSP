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

import gsp
from gsp import core, visual, glm
from gsp import transform
# import matplotlib.pyplot as plt
import numpy as np

canvas = core.Canvas(512, 512, 100.0)
viewport = core.Viewport(canvas, 0, 0, 512, 512, [1,1,1,1])
n = 2
P = glm.to_vec3(np.random.uniform(-1, +1, (n,2)), dtype=np.float32)



positions_np = np.random.uniform(-1, +1, (n,2))
# buffer_count = positions_np.size
# buffer_dtype = positions_np.dtype
# buffer_data = positions_np.data
# position_buffer = core.Buffer(buffer_count, buffer_dtype, buffer_data)

pixels = visual.Pixels(positions=P, colors=[0,0,0,1])
pixels.render(viewport)

import os
__dirname__ = os.path.dirname(os.path.abspath(__file__))
gsp.save(filename=f"{__dirname__}/output/pixels-2d.command.json",)

# from common.camera import Camera
# camera = Camera("ortho")
# camera.connect(viewport, "motion",  pixels.render)
# camera.save("output/pixels-2d.png")
# camera.run()