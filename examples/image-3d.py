import os
import matplotlib.pyplot as plt
import matplotlib.image as mpl_img

import gsp
from gsp.matplotlib import core, visual, glm
from gsp.transform import Transform
from gsp.core import Viewport, Buffer, Color, Matrix
import matplotlib.pyplot as plt
import numpy as np

# import gsp
gsp.use("matplotlib")

__dirname__ = os.path.dirname(os.path.abspath(__file__))

########################################################################################

canvas = core.Canvas(1024, 1024, 100.0)
viewport = core.Viewport(canvas, 0, 0, 1024, 1024, [1, 1, 1, 1])

######

cube_path_positions = glm.vec3(8)
cube_path_positions[...] = [
    (-1.0, -1.0, +1.0),
    (+1.0, -1.0, +1.0),
    (-1.0, +1.0, +1.0),
    (+1.0, +1.0, +1.0),
    (-1.0, -1.0, -1.0),
    (+1.0, -1.0, -1.0),
    (-1.0, +1.0, -1.0),
    (+1.0, +1.0, -1.0),
]
cube_path_face_indices = [
    [0, 1],
    [1, 3],
    [3, 2],
    [2, 0],
    [4, 5],
    [5, 7],
    [7, 6],
    [6, 4],
    [0, 4],
    [1, 5],
    [2, 6],
    [3, 7],
]

colormap = gsp.transform.Colormap("gray", vmin=0.0, vmax=0.75)
depth = gsp.transform.Out("screen[paths].z")
paths_visual = visual.Paths(
    cube_path_positions,
    cube_path_face_indices,
    line_colors=colormap(depth),
    line_widths=5.0 * (1 - 1.25 * depth),
    line_styles=gsp.core.LineStyle.solid,
    line_joins=gsp.core.LineJoin.round,
    line_caps=gsp.core.LineCap.round,
)
paths_visual.render(viewport)

#####################################################################
# Add an image visual
#

# Read the image_data numpy array from a file
image_path = f"{__dirname__}/images/UV_Grid_Sm.jpg"
image_data_np = mpl_img.imread(image_path)

image_visual = visual.Image(
    positions=[[-1, 1, -1]],
    image_data=image_data_np,
    image_extent=(-1, 1, -1, 1),
)
image_visual.render(viewport)

# plt.show()

#####################################################################
# Run the camera
#
from libs.camera import Camera

camera_ortho_enabled = False
if camera_ortho_enabled:
    camera = Camera("ortho")
    camera.connect(viewport, "motion", paths_visual.render)
    camera.connect(viewport, "motion", image_visual.render)
    camera.run()
else:
    camera = Camera("perspective", theta=0, phi=0)
    camera.connect(viewport, "motion", paths_visual.render)
    camera.connect(viewport, "motion", image_visual.render)
    camera.run()
