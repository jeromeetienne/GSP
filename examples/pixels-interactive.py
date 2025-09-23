# Package: Graphic Server Protocol
# Authors: Nicolas P .Rougier <nicolas.rougier@gmail.com>
# License: BSD 3 clause
"""
This example show the Pixels visual where pixels are spread
randomly inside a cube that can be rotated using the mouse.
"""
import numpy as np

from common.launcher import parse_args
from gsp_matplotlib import glm

# Parse command line arguments
core, visual, render = parse_args()

print("Warning: This example may take a while to render due to the large number of pixels.")

# Create a GSP scene
canvas = core.Canvas(512, 512, 100.0)
viewport = core.Viewport(canvas, 0, 0, 512, 512, [1,1,1,1])
n = 20_000
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

# Show or save the result
render(canvas, [viewport], [pixels])