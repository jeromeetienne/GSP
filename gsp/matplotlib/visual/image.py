# Package: Graphic Server Protocol / Matplotlib
# Authors: Nicolas P .Rougier <nicolas.rougier@gmail.com>
# License: BSD 3 clause

import numpy as np
from gsp import glm
from gsp import visual
from gsp.io.command import command
from gsp.transform import Transform
from gsp.core import  Buffer, Color, Matrix
import matplotlib.image as mpl_img
import gsp.matplotlib.core.viewport as Viewport


class Image(visual.Image):
    """
    TODO to write
    TODO port to matplotlib.core.Texture instead of np.ndarray directly
    """

    @command("visual.Image")
    def __init__(
        self,
        positions: Transform | Buffer,
        image_data: np.ndarray,
        image_extent: tuple[int, int, int, int] = (-1, 1, -1, 1),
    ):
        super().__init__(positions, image_data, image_extent, __no_command__=True)

        self._positions = positions
        self._image_data = image_data
        self._image_extent = image_extent

    def render(
        self,
        viewport: Viewport,
        model: Matrix | None = None,
        view: Matrix | None = None,
        proj: Matrix | None = None,
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
            axe_image = mpl_img.AxesImage(
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

        axe_image = self._viewports[viewport]
        positions4d = glm.to_vec4(self._positions) @ self._transform.T
        positions3d = glm.to_vec3(positions4d)
        # FIXME here image_extent is divided by W after rotation
        # but there is nothing to compensate for the camera z
        # - should i divide by the camera's zoom ?
        projected_extent = (
            positions3d[0, 0] + self._image_extent[0] / positions4d[0, 3],
            positions3d[0, 0] + self._image_extent[1] / positions4d[0, 3],
            positions3d[0, 1] + self._image_extent[2] / positions4d[0, 3],
            positions3d[0, 1] + self._image_extent[3] / positions4d[0, 3],
        )
        axe_image.set_extent(projected_extent)

        self.set_variable("screen[positions]", positions3d)

        # Restore tracking
        glm.ndarray.tracked.__tracker_class__ = tracker
