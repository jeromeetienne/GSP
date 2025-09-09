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

from gsp.matplotlib import core, visual, glm
from gsp import transform
import matplotlib.pyplot as plt
import numpy as np


canvas = core.Canvas(512, 512, 100.0)
viewport = core.Viewport(canvas, 0, 0, 512, 512, [1,1,1,1])
n_points = 250_000
positions_np = np.random.uniform(-1, +1, (n_points,3))
positions_vec3 = glm.to_vec3(positions_np)


buffer_count = positions_vec3.shape[0] * positions_vec3.shape[1]
buffer_dtype = positions_vec3.dtype
buffer_data = positions_vec3.data
position_buffer = gsp.core.Buffer(buffer_count, buffer_dtype, buffer_data)

pixels = visual.Pixels(positions_vec3, colors=[0,0,0,1])
# pixels = visual.Pixels(position_buffer, colors=[0,0,0,1])
# pixels.render(viewport)


# import matplotlib.pyplot as plt
# plt.savefig("output/pixels-2d-io2.png")

import os
__dirname__ = os.path.dirname(os.path.abspath(__file__))

image_filename = f"{__dirname__}/output/pixels-2d-io.png"



from libs.camera import Camera
camera = Camera("perpective")
camera.connect(viewport, "motion",  pixels.render)
camera.save(image_filename)
camera.run()