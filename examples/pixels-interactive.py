# Package: Graphic Server Protocol
# Authors: Nicolas P .Rougier <nicolas.rougier@gmail.com>
# License: BSD 3 clause
"""
This example show the Pixels visual where pixels are spread
randomly inside a cube that can be rotated using the mouse.
"""
# Experiment to handle intellisense in VSCode
from gsp.matplotlib import core, visual, glm
import matplotlib.pyplot as plt
import numpy as np

import gsp
gsp.use("matplotlib")

canvas = core.Canvas(512, 512, 100.0)
viewport = core.Viewport(canvas, 0, 0, 512, 512, [1,1,1,1])
n = 250_000
P = glm.as_vec3(np.random.uniform(-1, +1, (n,3)))
pixels = visual.Pixels(P, colors=[0,0,0,1])
pixels.render(viewport)

# -----------------------------------
# gsp.save("session.json")
# plt.close()
# queue = gsp.load("session.json")
# queue.run(globals(), locals())
# canvas = gsp.Object.objects[canvas.id]
# viewport = gsp.Object.objects[viewport.id]
# pixels = gsp.Object.objects[pixels.id]
# -----------------------------------

# Run the camera
from common.camera import Camera
camera = Camera("perspective", theta=50, phi=50)
camera.connect(viewport, "motion",  pixels.render)
camera.run()
