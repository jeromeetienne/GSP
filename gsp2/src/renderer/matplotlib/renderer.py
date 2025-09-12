from ...visuals.pixels import Pixels
from ...visuals.image import Image
from ...core.canvas import Canvas
import matplotlib.pyplot as plt
import matplotlib.axes as mpl_axes


class MatplotlibRenderer:
    def __init__(self):
        pass

    def render(self, canvas: Canvas, image_filename: str | None = None, show_image: bool = True) -> None:

        figure = plt.figure(frameon=False, dpi=canvas.dpi)
        figure.set_size_inches(canvas.width / canvas.dpi, canvas.height / canvas.dpi)

        axes: mpl_axes.Axes = figure.add_axes((0, 0, 1, 1))
        axes.set_xlim(-1, 1)
        axes.set_ylim(-1, 1)
        axes.get_xaxis().set_visible(False)
        axes.get_yaxis().set_visible(False)

        for viewport in canvas.viewports:
            for visual in viewport.visuals:
                if isinstance(visual, Pixels):
                    self.__render_pixels(axes, visual)
                elif isinstance(visual, Image):
                    self.__render_image(axes, visual)
                else:
                    raise NotImplementedError(
                        f"Rendering for visual type {type(visual)} is not implemented."
                    )

        # Save to file
        if image_filename is not None:
            figure.savefig(image_filename, dpi=canvas.dpi)

        if show_image:
            plt.show(block=True)


    def __render_pixels(self, axes: mpl_axes.Axes, pixels: Pixels) -> None:
        positions = pixels.positions
        colors = pixels.colors
        sizes = pixels.sizes
        pathCollection = axes.scatter(positions[:, 0], positions[:, 1], s=sizes, c=[colors], cmap='gray')

    def __render_image(self, axes: mpl_axes.Axes, image: Image) -> None:
        bounds = image.bounds
        image_data = image.image_data
        extent = (bounds[0], bounds[1], bounds[2], bounds[3])
        axes.imshow(image_data, extent=extent, origin="lower")
