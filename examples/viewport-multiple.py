# Package: Graphic Server Protocol
# Authors: Nicolas P .Rougier <nicolas.rougier@gmail.com>
# License: BSD 3 clause
"""
Multiple viewports
==================

This example show how to have several viewports.
"""
# Experiment to handle intellisense in VSCode
from gsp.matplotlib import core, visual, glm
import matplotlib.pyplot as plt
import numpy as np

import gsp
gsp.use("matplotlib")

canvas = core.Canvas(512, 512, 100.0)

# Fixed viewport sizes and positions (in pixels)
# core.Viewport(canvas, 0, 0, 256, 256, (1,0,0,1))
# core.Viewport(canvas, 0, 256, 256, 256, (0,1,0,1))
# core.Viewport(canvas, 256, 0, 256, 256, (0,0,1,1))
# core.Viewport(canvas, 256, 256, 256, 256, (1,1,0,1))

# Proportional viewport sizes and positions
core.Viewport(canvas, 0.0, 0.0, 0.5, 0.5, (1,0,0,1))
core.Viewport(canvas, 0.0, 0.5, 0.5, 0.5, (0,1,0,1))
core.Viewport(canvas, 0.5, 0.0, 0.5, 0.5, (0,0,1,1))
core.Viewport(canvas, 0.5, 0.5, 0.5, 0.5, (1,1,0,1))

canvas.render("./output/viewport-multiple.png")
plt.show()
