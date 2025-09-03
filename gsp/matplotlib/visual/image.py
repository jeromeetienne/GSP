# Package: Graphic Server Protocol / Matplotlib
# Authors: Nicolas P .Rougier <nicolas.rougier@gmail.com>
# License: BSD 3 clause

import numpy as np
from gsp import glm
from gsp import visual
from gsp.io.command import command
from gsp.transform import Transform
from gsp.core import Viewport, Buffer, Color, Matrix
import matplotlib.image as mplimg


class Image(visual.Image):
    """
    TODO to write
    """

    @command("visual.Image")
    def __init__(
        self, positions: Transform | Buffer, image_path: str
    ):
        super().__init__(positions, __no_command__=True)

        self._image = mplimg.imread(image_path)

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

        # Disable tracking for newly created glm.ndarray (or else,
        # this will create GSP buffers)
        tracker = glm.ndarray.tracked.__tracker_class__
        glm.ndarray.tracked.__tracker_class__ = None

        # Create the collection if necessary
        if viewport not in self._viewports:
            axe_image = mplimg.AxesImage(
                viewport._axes,
                extent=[-1, 1, -1, 1],
                origin="upper",
                clip_on=True,
                interpolation="nearest",
                zorder=0,
                data=self._image,
            )
            self._viewports[viewport] = axe_image
            viewport._axes.add_image(axe_image)

            # This is necessary for measure transforms that need to be
            # kept up to date with canvas size
            # canvas = viewport._canvas._figure.canvas
            # canvas.mpl_connect("resize_event", lambda event: self.render(viewport))

        # If render has been called without model/view/proj, we don't
        # render Such call is only used to declare that this visual is
        # to be rendered on that viewport.
        if self._transform is None:
            # Restore tracking
            glm.ndarray.tracked.__tracker_class__ = tracker
            return

    #     axe_image = self._viewports[viewport]
    #     positions = glm.to_vec3(glm.to_vec4(self._positions) @ self._transform.T)
    #     image_extent = (positions[0,0]-0.5, positions[0,0]+0.5, positions[0,1]-0.5, positions[0,1]+0.5)
    #     axe_image.set_extent(image_extent)
    #     # print(image_extent)
    #     # plt.imshow(self._image, extent=imshow_extent)

    #     # plt.imshow(self._image, extent=(-0.5, 0.5, -0.5, 0.5))

    #     print('ddd')

        axe_image = self._viewports[viewport]
        positions = self.eval_variable("positions")
        # positions = positions.reshape(-1,3)
        positions = glm.to_vec3(glm.to_vec4(positions) @ self._transform.T)
        image_extent = (positions[0,0]-0.5, positions[0,0]+0.5, positions[0,1]-0.5, positions[0,1]+0.5)
        # image_extent = [-1, 1, -1, 1]
        axe_image.set_extent(image_extent)

        self.set_variable("screen[positions]", positions)

        # Restore tracking
        glm.ndarray.tracked.__tracker_class__ = tracker
