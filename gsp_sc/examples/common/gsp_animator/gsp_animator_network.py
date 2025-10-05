# stdlib imports
import io
from typing import Callable

# pip imports
import numpy as np
import matplotlib.pyplot
import matplotlib.image
import matplotlib.animation

# local imports
import gsp_sc.src as gsp_sc
from gsp_sc.src.core import canvas
from .gsp_animator_types import GSPAnimatorFunc


class GSPAnimatorNetwork:
    """
    Animator for GSP scenes using a network renderer and matplotlib for display.

    Note: this requires a running GSP server. See the README for instructions.
    Note: it uses pip matplotlib, not the GSP matplotlib renderer.
    """

    def __init__(self, network_renderer: gsp_sc.renderer.network.NetworkRenderer):
        self._network_renderer = network_renderer

    def animate(self, canvas: gsp_sc.core.Canvas, camera: gsp_sc.core.Camera, animator_callbacks: list[GSPAnimatorFunc]):
        """
        Animate the given canvas and camera using the provided callbacks to update visuals.
        """

        # create a matplotlib figure of the right size
        figure = matplotlib.pyplot.figure(frameon=False, dpi=canvas.dpi)
        figure.set_size_inches(canvas.width / canvas.dpi, canvas.height / canvas.dpi)

        # get the only axes in the figure
        mpl_axes = figure.add_axes((0, 0, 1, 1))

        # create an np.array to hold the image
        image_data_np = np.zeros((canvas.height, canvas.width, 3), dtype=np.uint8)
        axes_image = mpl_axes.imshow(image_data_np)

        # function called at each animation frame
        def mpl_animate(frame_index: int):
            # notify all animator callbacks
            changed_visuals: list[gsp_sc.core.VisualBase] = []
            for callback in animator_callbacks:
                _changed_visuals = callback()
                changed_visuals.extend(_changed_visuals)

            # render the scene to get the new image
            image_png_data = self._network_renderer.render(canvas, camera)
            image_data_io = io.BytesIO(image_png_data)
            image_data_np = matplotlib.image.imread(image_data_io, format="png")

            # update the image data
            axes_image.set_data(image_data_np)

            # return the changed mpl artists
            changed_mpl_artists = [axes_image]
            return changed_mpl_artists

        anim = matplotlib.animation.FuncAnimation(figure, mpl_animate, frames=100, interval=1000.0 / 30)

        matplotlib.pyplot.axis("off")
        matplotlib.pyplot.show()
