import io

from ...visuals.pixels import Pixels
from ...visuals.image import Image
from ...core.canvas import Canvas
import matplotlib.pyplot as plt
import matplotlib.axes as mpl_axes


class MatplotlibRenderer:
    def __init__(self) -> None: 
        pass

    def render(self, canvas: Canvas, show_image: bool = True, return_image: bool = False) -> bytes:

        figure = plt.figure(frameon=False, dpi=canvas.dpi)
        figure.set_size_inches(canvas.width / canvas.dpi, canvas.height / canvas.dpi)

        for viewport in canvas.viewports:
            axes_rect = (viewport.origin_x / canvas.width,
                         viewport.origin_y / canvas.height,
                         viewport.width / canvas.width,
                         viewport.height / canvas.height)
            axes: mpl_axes.Axes = figure.add_axes(axes_rect)
            axes.set_xlim(-1, 1)
            axes.set_ylim(-1, 1)
            axes.get_xaxis().set_visible(False)
            axes.get_yaxis().set_visible(False)

            # axes.set_position((viewport.x, viewport.y, viewport.width, viewport.height))

            for visual in viewport.visuals:
                if isinstance(visual, Pixels):
                    self.__render_pixels(axes, visual)
                elif isinstance(visual, Image):
                    self.__render_image(axes, visual)
                else:
                    raise NotImplementedError(
                        f"Rendering for visual type {type(visual)} is not implemented."
                    )

        # honor show_image option
        if show_image:
            plt.show(block=True)

        image_png_data = b""

        # honor return_image option
        if return_image:
            # Render the image to a PNG buffer
            image_png_buffer = io.BytesIO()
            plt.savefig(image_png_buffer, format='png')
            image_png_buffer.seek(0)
            image_png_data = image_png_buffer.getvalue()
            image_png_buffer.close()

        # return the PNG image data if requested else return empty bytes
        return image_png_data


    def __render_pixels(self, axes: mpl_axes.Axes, pixels: Pixels) -> None:
        positions = pixels.positions
        colors = pixels.colors
        sizes = pixels.sizes
        pathCollection = axes.scatter(positions[:, 0], positions[:, 1], s=sizes, c=[colors])

    def __render_image(self, axes: mpl_axes.Axes, image: Image) -> None:
        bounds = image.image_extent
        image_data = image.image_data
        extent = (bounds[0], bounds[1], bounds[2], bounds[3])
        axes.imshow(image_data, extent=extent, origin="lower")
