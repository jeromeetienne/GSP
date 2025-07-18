# Package: Graphic Server Protocol
# Authors: Nicolas P .Rougier <nicolas.rougier@gmail.com>
# License: BSD 3 clause
"""
Paths visual (3D)
=================

This example shows the Paths visual using a wireframe cube whose edges
width and color are dependent on the depth. The cube can be rotated
and zoomed using the mouse and a perspective camera.

"""
# Experiment to handle intellisense in VSCode
from gsp import core, transform, visual, glm
import matplotlib.pyplot as plt
import numpy as np

import gsp
gsp.use("matplotlib")

black, white = [0,0,0,1], [1,1,1,1]
canvas = core.Canvas(512, 512, 100.0)
viewport = core.Viewport(canvas, 0, 0, 512, 512, [1,1,1,1])

P = glm.vec3(8)
P[...] = [(-1.0, -1.0, +1.0), (+1.0, -1.0, +1.0), 
          (-1.0, +1.0, +1.0), (+1.0, +1.0, +1.0), 
          (-1.0, -1.0, -1.0), (+1.0, -1.0, -1.0),
          (-1.0, +1.0, -1.0), (+1.0, +1.0, -1.0) ]
I = [ [0,1], [1,3], [3,2], [2,0],
      [4,5], [5,7], [7,6], [6,4],
      [0,4], [1,5], [2,6], [3,7] ]

colormap = transform.Colormap("gray",vmin=0.0, vmax=0.75)
depth = transform.Out("screen[paths].z")
paths = visual.Paths(P, I,
                     line_colors = colormap(depth),
                     line_widths = 5.0*(1 - 1.25*depth),
                     line_styles = gsp.core.LineStyle.solid,
                     line_joins = gsp.core.LineJoin.round,
                     line_caps = gsp.core.LineCap.round)

from libs.camera import Camera
camera = Camera("perspective", theta=50, phi=50, zoom = 1.25)
camera.connect(viewport, "motion",  paths.render)
# camera.save("output/paths-3d.png")
camera.run()
