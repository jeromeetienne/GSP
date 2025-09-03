import os
import matplotlib.pyplot as plt
import matplotlib.image as mplimg

import gsp
from gsp.matplotlib import core, visual, glm
from gsp.transform import Transform
from gsp.core import Viewport, Buffer, Color, Matrix
import matplotlib.pyplot as plt


########################################################################################
# plt.imshow(mpl_image)
# plt.axis('off')  # Hide axes
# plt.show()

import numpy as np

# import gsp
# gsp.use("matplotlib")

__dirname__ = os.path.dirname(os.path.abspath(__file__))

# Replace with your image path
image_path = f"{__dirname__}/images/UV_Grid_Sm.jpg"
mpl_image = mplimg.imread(image_path)
# rescale mpl_image resolution from 1024x1024 to 1x1
# mpl_image = np.resize(mpl_image, (1, 1, 4))

# plt.axis('off')  # Hide axes


canvas = core.Canvas(1024, 1024, 100.0)
viewport = core.Viewport(canvas, 0, 0, 1024, 1024, [1, 1, 1, 1])

######
point_count = 50_000
point_positions = glm.as_vec3(np.random.uniform(-1, +1, (point_count, 3)))
pixels = visual.Pixels(point_positions, colors=[1, 0, 0, 0.5])
pixels.render(viewport)

#######


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
paths = visual.Paths(
    cube_path_positions,
    cube_path_face_indices,
    line_colors=colormap(depth),
    line_widths=5.0 * (1 - 1.25 * depth),
    line_styles=gsp.core.LineStyle.solid,
    line_joins=gsp.core.LineJoin.round,
    line_caps=gsp.core.LineCap.round,
)


#######

# plt.imshow(mpl_image, extent=(-1, 1, -1, 1))

from gsp.visual.image import Image

from gsp.visual.image import Image as Visual_image
from gsp.visual.visual import Visual


class Image_local(Visual_image):
    def __init__(
        self,
        positions: Transform | Buffer,
        image_path: str,
        image_extent: tuple = (-1, 1, -1, 1),
    ):
        super().__init__(positions, __no_command__=True)

        self._image_data = mplimg.imread(image_path)
        self._image_extent = image_extent
        self._positions = positions

    def render(
        self,
        viewport: Viewport,
        model: Matrix = None,
        view: Matrix = None,
        proj: Matrix = None,
    ):
        super().render(viewport, model, view, proj)

        model = model if model is not None else self._model
        view = view if view is not None else self._view
        proj = proj if proj is not None else self._proj

        # Create the collection if necessary
        if viewport not in self._viewports:
            # axe_image = viewport._axes.imshow(self._image)
            axe_image = mplimg.AxesImage(
                viewport._axes,
                # extent=[-1, 1, -1, 1],
                # origin="upper",
                # clip_on=True,
                # interpolation="nearest",
                # zorder=0,
                data=self._image_data,
            )
            self._viewports[viewport] = axe_image
            viewport._axes.add_image(axe_image)

        axe_image = self._viewports[viewport]
        positions4d = glm.to_vec4(self._positions) @ self._transform.T
        positions3d = glm.to_vec3(positions4d)

        # image_extent = (positions[0,0]-0.5, positions[0,0]+0.5, positions[0,1]-0.5, positions[0,1]+0.5)

        
        projected_extent = (
            positions3d[0, 0] + self._image_extent[0]/positions4d[0, 3],
            positions3d[0, 0] + self._image_extent[1]/positions4d[0, 3],
            positions3d[0, 1] + self._image_extent[2]/positions4d[0, 3],
            positions3d[0, 1] + self._image_extent[3]/positions4d[0, 3],
        )
        axe_image.set_extent(projected_extent)

        print("ddd")


# gsp_image = Image_local(
#     positions=[[1, 1, 1], image_path=image_path, image_extent=(-0.5, 0.5, -0.5, 0.5)
# )

gsp_images = []
image_extent = (-3.15, 3.15, -3.15, 3.15)
gsp_images.append(
    Image_local(
        positions=[[-1, 1, -1]],
        image_path=image_path,
        image_extent=image_extent,
    )
)
gsp_images.append(
    Image_local(
        positions=[[1, 1, -1]],
        image_path=image_path,
        image_extent=image_extent,
    )
)
# gsp_image.render(viewport)


def render_local(
    viewport: Viewport, model: Matrix = None, view: Matrix = None, proj: Matrix = None
):
    paths.render(viewport, model, view, proj)
    pixels.render(viewport, model, view, proj)
    for gsp_image in gsp_images:
        gsp_image.render(viewport, model, view, proj)


# Run the camera
from libs.camera import Camera

# camera = Camera("perspective", theta=50, phi=50)
camera = Camera("perspective", theta=0, phi=0)
# camera = Camera("ortho")
camera.connect(viewport, "motion", render_local)
camera.run()
