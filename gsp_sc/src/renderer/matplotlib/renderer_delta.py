import io


import mpl3d.glm

from ...visuals.pixels import Pixels
from ...visuals.image import Image
from ...core.canvas import Canvas
from ...core.visual_base import VisualBase

import matplotlib.pyplot
import matplotlib.axes 
import matplotlib.figure
import matplotlib.collections
import matplotlib.image

import numpy as np


class MatplotlibRendererDelta:
    def __init__(self) -> None:
        self._figures: dict[str, matplotlib.figure.Figure] = {}
        self._axes: dict[str, matplotlib.axes.Axes] = {}
        self._pathCollections: dict[str, matplotlib.collections.PathCollection] = {}
        self._axesImages: dict[str, matplotlib.image.AxesImage] = {}


    def render(self, canvas: Canvas, transform_matrix: np.ndarray | None = None, show_image: bool = True, return_image: bool = False) -> bytes:

        if canvas.uuid in self._figures:
            figure = self._figures[canvas.uuid]
        else:
            print("Creating new figure")
            figure = matplotlib.pyplot.figure(frameon=False, dpi=canvas.dpi)
            figure.set_size_inches(canvas.width / canvas.dpi, canvas.height / canvas.dpi)
            self._figures[canvas.uuid] = figure

        for viewport in canvas.viewports:
            # create an axes for each viewport
            if viewport.uuid in self._axes:
                axes = self._axes[viewport.uuid]
            else:
                print("Creating new axes for viewport")
                axes_rect = (viewport.origin_x / canvas.width,
                            viewport.origin_y / canvas.height,
                            viewport.width / canvas.width,
                            viewport.height / canvas.height)
                axes: matplotlib.axes.Axes = figure.add_axes(axes_rect)
                axes.set_xlim(-1, 1)
                axes.set_ylim(-1, 1)
                axes.get_xaxis().set_visible(False)
                axes.get_yaxis().set_visible(False)
                self._axes[viewport.uuid] = axes


            for visual in viewport.visuals:
                if isinstance(visual, Pixels):
                    self.__render_pixels(axes, visual, transform_matrix)
                elif isinstance(visual, Image):
                    self.__render_image(axes, visual)
                else:
                    raise NotImplementedError(
                        f"Rendering for visual type {type(visual)} is not implemented."
                    )

        figure.canvas.draw()

        # honor show_image option
        # if show_image:
        #     plt.show(block=True)

        image_png_data = b""

        # honor return_image option
        if return_image:
            # Render the image to a PNG buffer
            image_png_buffer = io.BytesIO()
            matplotlib.pyplot.savefig(image_png_buffer, format='png')
            image_png_buffer.seek(0)
            image_png_data = image_png_buffer.getvalue()
            image_png_buffer.close()

        # return the PNG image data if requested else return empty bytes
        return image_png_data


    def __render_pixels(self, axes: matplotlib.axes.Axes, pixels: Pixels, transform_matrix: np.ndarray | None = None) -> None:
        if pixels.uuid not in self._pathCollections:
            print("Creating new PathCollection for pixels visual")
            self._pathCollections[pixels.uuid] = axes.scatter([], [])

        pathCollection = self._pathCollections[pixels.uuid]
        if transform_matrix is not None:

            transformed_positions:np.ndarray = mpl3d.glm.transform(pixels.positions, transform_matrix)
            pathCollection.set_offsets(transformed_positions)
        else:
            pathCollection.set_offsets(pixels.positions)

        pathCollection.set_sizes(pixels.sizes)
        pathCollection.set_color(pixels.colors)

    def __render_image(self, axes: matplotlib.axes.Axes, image: Image) -> None:
        if image.uuid not in self._axesImages:
            print("Creating new AxesImage for image visual")
            self._axesImages[image.uuid] = matplotlib.image.AxesImage(
                axes,
                extent=(-1, 1, -1, 1),
                # origin="upper",
                # clip_on=True,
                # interpolation="nearest",
                # zorder=0,
                data=image.image_data,
            )

        axes_image = self._axesImages[image.uuid]
        axes_image.set_data(image.image_data)

        extent = (image.bounds[0], image.bounds[1], image.bounds[2], image.bounds[3])
        axes_image.set_extent(extent)
