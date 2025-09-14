import io
import os


import mpl3d.glm
import mpl3d.camera

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


class MatplotlibRenderer:
    def __init__(self) -> None:
        self._figures: dict[str, matplotlib.figure.Figure] = {}
        self._axes: dict[str, matplotlib.axes.Axes] = {}
        self._pathCollections: dict[str, matplotlib.collections.PathCollection] = {}
        self._axesImages: dict[str, matplotlib.image.AxesImage] = {}

    def render(
        self,
        canvas: Canvas,
        camera: mpl3d.camera.Camera | None = None,
        show_image: bool = False,
        return_image: bool = True,
        interactive: bool = False,
    ) -> bytes:

        self.__render(canvas, camera=camera)

        ################################################################################

        # honor show_image option
        if show_image:
            # enter the matplotlib main loop IIF env.var GSP_SC_INTERACTIVE is not set to "False"
            if (
                "GSP_SC_INTERACTIVE" not in os.environ
                or os.environ["GSP_SC_INTERACTIVE"] != "False"
            ):
                matplotlib.pyplot.show(block=True)

        if interactive and camera is not None:
            figure = matplotlib.pyplot.gcf()
            mpl_axes = figure.get_axes()[0]

            # connect the camera events to the render function
            def camera_update(transform) -> None:
                self.render(canvas, camera=camera, show_image=False)

            camera.connect(mpl_axes, camera_update)
            # enter the matplotlib main loop IIF env.var GSP_SC_INTERACTIVE is not set to "False"
            if (
                "GSP_SC_INTERACTIVE" not in os.environ
                or os.environ["GSP_SC_INTERACTIVE"] != "False"
            ):
                matplotlib.pyplot.show(block=True)

        image_png_data = b""

        # honor return_image option
        if return_image:
            # Render the image to a PNG buffer
            image_png_buffer = io.BytesIO()
            matplotlib.pyplot.savefig(image_png_buffer, format="png")
            image_png_buffer.seek(0)
            image_png_data = image_png_buffer.getvalue()
            image_png_buffer.close()

        # return the PNG image data if requested else return empty bytes
        return image_png_data

    def __render(
        self,
        canvas: Canvas,
        camera: mpl3d.camera.Camera | None = None,
    ) -> None:
        if canvas.uuid in self._figures:
            figure = self._figures[canvas.uuid]
        else:
            print(f"Creating new figure {canvas.uuid}")
            figure = matplotlib.pyplot.figure(frameon=False, dpi=canvas.dpi)
            figure.set_size_inches(
                canvas.width / canvas.dpi, canvas.height / canvas.dpi
            )
            self._figures[canvas.uuid] = figure

        for viewport in canvas.viewports:
            # create an axes for each viewport
            if viewport.uuid in self._axes:
                axes = self._axes[viewport.uuid]
            else:
                print(f"Creating new axes for viewport {viewport.uuid}")
                axes_rect = (
                    viewport.origin_x / canvas.width,
                    viewport.origin_y / canvas.height,
                    viewport.width / canvas.width,
                    viewport.height / canvas.height,
                )
                axes: matplotlib.axes.Axes = figure.add_axes(axes_rect)
                axes.set_xlim(-1, 1)
                axes.set_ylim(-1, 1)
                axes.get_xaxis().set_visible(False)
                axes.get_yaxis().set_visible(False)
                self._axes[viewport.uuid] = axes

            for visual in viewport.visuals:
                if isinstance(visual, Pixels):
                    self.__render_pixels(
                        axes,
                        visual,
                        full_uuid=visual.uuid + viewport.uuid,
                        camera=camera,
                    )
                elif isinstance(visual, Image):
                    self.__render_image(
                        axes,
                        visual,
                        full_uuid=visual.uuid + viewport.uuid,
                        camera=camera,
                    )
                else:
                    raise NotImplementedError(
                        f"Rendering for visual type {type(visual)} is not implemented."
                    )

    def __render_pixels(
        self,
        axes: matplotlib.axes.Axes,
        pixels: Pixels,
        full_uuid: str,
        camera: mpl3d.camera.Camera | None = None,
    ) -> None:
        if full_uuid in self._pathCollections:
            pathCollection = self._pathCollections[full_uuid]
        else:
            print(f"Creating new PathCollection for pixels visual {full_uuid}")
            pathCollection = axes.scatter([], [])
            self._pathCollections[full_uuid] = pathCollection

        if camera is not None:
            transformed_positions: np.ndarray = mpl3d.glm.transform(
                pixels.positions, camera.transform
            )
            pathCollection.set_offsets(transformed_positions)
        else:
            pathCollection.set_offsets(pixels.positions)

        pathCollection.set_sizes(pixels.sizes)
        pathCollection.set_color(pixels.colors)

    def __render_image(
        self,
        axes: matplotlib.axes.Axes,
        image: Image,
        full_uuid: str,
        camera: mpl3d.camera.Camera | None = None,
    ) -> None:
        if full_uuid not in self._axesImages:
            print(f"Creating new AxesImage for image visual {full_uuid}")
            self._axesImages[full_uuid] = axes.imshow(np.zeros((2, 2, 3)))

        axes_image = self._axesImages[full_uuid]
        axes_image.set_data(image.image_data)

        #

        if camera is not None:
            # extent_3d = np.array([
            #     [image.position[0]+image.image_extent[0], image.position[1]+image.image_extent[2], image.position[2]],
            #     [image.position[0]+image.image_extent[1], image.position[1]+image.image_extent[2], image.position[2]],
            #     [image.position[0]+image.image_extent[1], image.position[1]+image.image_extent[3], image.position[2]],
            #     [image.position[0]+image.image_extent[0], image.position[1]+image.image_extent[3], image.position[2]],
            # ])

            # transformed_positions: np.ndarray = mpl3d.glm.transform(
            #     V=extent_3d, mvp=camera.transform
            # )
            # transformed_extent = (
            #     transformed_positions[0, 0],
            #     transformed_positions[0, 1],
            #     transformed_positions[0, 2],
            #     transformed_positions[0, 3],
            # )
            # axes_image.set_extent(transformed_extent)

            positions = np.array([image.position])
            transformed_positions: np.ndarray = mpl3d.glm.transform(
                positions, camera.transform
            )
            # FIXME should be divided by W after rotation
            # but there is nothing to compensate for the camera z
            transformed_extent = (
                transformed_positions[0, 0] + image.image_extent[0],
                transformed_positions[0, 0] + image.image_extent[1],
                transformed_positions[0, 1] + image.image_extent[2],
                transformed_positions[0, 1] + image.image_extent[3],
            )
            axes_image.set_extent(transformed_extent)
        else:
            extent = (
                image.image_extent[0],
                image.image_extent[1],
                image.image_extent[2],
                image.image_extent[3],
            )
            axes_image.set_extent(extent)
