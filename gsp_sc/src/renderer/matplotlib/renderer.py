# stdlib imports
import io
import os
import numpy as np
import typing

# pip imports
import matplotlib.collections
import matplotlib.colors
import matplotlib.pyplot
import matplotlib.axes
import matplotlib.figure
import matplotlib.collections
import matplotlib.image
import mpl3d.glm
import mpl3d.camera

# local imports
from ...core.canvas import Canvas
from ...core.viewport import Viewport
from ...core.visual_base import VisualBase
from ...core.camera import Camera
from ...visuals.pixels import Pixels
from ...visuals.image import Image
from ...visuals.mesh import Mesh
from ...transform import TransformChain


class MatplotlibRenderer:
    def __init__(self) -> None:
        self._figures: dict[str, matplotlib.figure.Figure] = {}
        """Mapping from canvas UUID to matplotlib Figure"""
        self._axes: dict[str, matplotlib.axes.Axes] = {}
        """Mapping from viewport UUID to matplotlib Axes"""
        self._pathCollections: dict[str, matplotlib.collections.PathCollection] = {}
        """Mapping from visual UUID to matplotlib PathCollection. For Pixels visuals."""
        self._polyCollections: dict[str, matplotlib.collections.PolyCollection] = {}
        """Mapping from visual UUID to matplotlib PolyCollection. For Mesh visuals."""
        self._axesImages: dict[str, matplotlib.image.AxesImage] = {}
        """Mapping from visual UUID to matplotlib AxesImage. For Image visuals."""

    def render(
        self,
        canvas: Canvas,
        camera: Camera,
        show_image: bool = False,
        return_image: bool = True,
        interactive: bool = False,
    ) -> bytes:
        result = self.render_viewports(
            canvas,
            viewports=canvas.viewports,
            cameras=[camera for _ in canvas.viewports],
            show_image=show_image,
            return_image=return_image,
            interactive=interactive,
        )
        return result

    def render_viewports(
        self,
        canvas: Canvas,
        viewports: list[Viewport],
        cameras: list[Camera],
        show_image: bool = False,
        return_image: bool = True,
        interactive: bool = False,
    ) -> bytes:

        self.__render(canvas, viewports=viewports, cameras=cameras)

        ################################################################################

        # honor show_image option
        if show_image:
            # enter the matplotlib main loop IIF env.var GSP_SC_INTERACTIVE is not set to "False"
            if "GSP_SC_INTERACTIVE" not in os.environ or os.environ["GSP_SC_INTERACTIVE"] != "False":
                matplotlib.pyplot.show(block=True)

        # Handle interactive camera IIF env.var GSP_SC_INTERACTIVE is not set to "False"
        if interactive and ("GSP_SC_INTERACTIVE" not in os.environ or os.environ["GSP_SC_INTERACTIVE"] != "False"):
            figure = matplotlib.pyplot.gcf()
            mpl_axes = figure.get_axes()[0]

            mpl3d_cameras: list[mpl3d.camera.Camera] = [camera.mpl3d_camera for camera in cameras]

            # connect the camera events to the render function
            def camera_update(transform) -> None:
                self.__render(canvas, viewports=viewports, cameras=cameras)

            for mpl3d_camera in mpl3d_cameras:
                mpl3d_camera.connect(mpl_axes, camera_update)

            matplotlib.pyplot.show(block=True)

            for mpl3d_camera in mpl3d_cameras:
                mpl3d_camera.disconnect()

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

    ###########################################################################
    ###########################################################################
    # .__render() and helpers
    ###########################################################################
    ###########################################################################

    def __render(
        self,
        canvas: Canvas,
        viewports: typing.List[Viewport],
        cameras: typing.List[Camera],
    ) -> None:
        # Create the matplotlib figure from the canvas if it does not exist yet
        if canvas.uuid in self._figures:
            figure = self._figures[canvas.uuid]
        else:
            # print(f"Creating new figure {canvas.uuid}")
            figure = matplotlib.pyplot.figure(frameon=False, dpi=canvas.dpi)
            figure.set_size_inches(canvas.width / canvas.dpi, canvas.height / canvas.dpi)
            self._figures[canvas.uuid] = figure

        # sanity check - viewports and cameras must have the same length
        assert len(viewports) == len(cameras), "Number of viewports must be equal to number of cameras."

        for viewport, camera in zip(viewports, cameras):
            # create an axes for each viewport
            if viewport.uuid in self._axes:
                axes = self._axes[viewport.uuid]
            else:
                # print(f"Creating new axes for viewport {viewport.uuid}")
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
                full_uuid = visual.uuid + viewport.uuid
                if isinstance(visual, Pixels):
                    self.__render_pixels(
                        axes,
                        visual,
                        full_uuid=full_uuid,
                        camera=camera,
                    )
                elif isinstance(visual, Image):
                    self.__render_image(
                        axes,
                        visual,
                        full_uuid=full_uuid,
                        camera=camera,
                    )
                elif isinstance(visual, Mesh):
                    self.__render_mesh(
                        axes,
                        visual,
                        full_uuid=full_uuid,
                        camera=camera,
                    )
                else:
                    raise NotImplementedError(f"Rendering for visual type {type(visual)} is not implemented.")

    def __render_pixels(
        self,
        axes: matplotlib.axes.Axes,
        pixels: Pixels,
        full_uuid: str,
        camera: Camera,
    ) -> None:
        # Notify pre-rendering event
        # TODO add the renderer object as sender?
        pixels.pre_rendering.send()

        if full_uuid in self._pathCollections:
            pathCollection = self._pathCollections[full_uuid]
        else:
            # print(f"Creating new PathCollection for pixels visual {full_uuid}")
            pathCollection = axes.scatter([], [])
            self._pathCollections[full_uuid] = pathCollection

        # compute positions
        pixel_positions = pixels.positions
        if type(pixel_positions) is TransformChain:
            pixel_positions = pixel_positions.run()
        else:
            pixel_positions = typing.cast(np.ndarray, pixel_positions)

        transformed_positions: np.ndarray = mpl3d.glm.transform(pixel_positions, camera.transform)

        # Notify post-transform event
        pixels.post_transform.send(
            self,
            **{
                "camera": camera,
                "transformed_positions": transformed_positions,
            },
        )

        pathCollection.set_offsets(transformed_positions)
        pathCollection.set_sizes(pixels.sizes)
        pathCollection.set_color(pixels.colors.tolist())
        # pathCollection.set_edgecolor([0,0,0,1])

        # Notify post-rendering event
        pixels.post_rendering.send()

    def __render_image(
        self,
        axes: matplotlib.axes.Axes,
        image: Image,
        full_uuid: str,
        camera: Camera,
    ) -> None:
        if full_uuid not in self._axesImages:
            # print(f"Creating new AxesImage for image visual {full_uuid}")
            self._axesImages[full_uuid] = axes.imshow(np.zeros((2, 2, 3)))

        axes_image = self._axesImages[full_uuid]
        axes_image.set_data(image.image_data)

        #

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
        transformed_positions: np.ndarray = mpl3d.glm.transform(positions, camera.transform)
        # FIXME should be divided by W after rotation
        # but there is nothing to compensate for the camera z
        transformed_extent = (
            transformed_positions[0, 0] + image.image_extent[0],
            transformed_positions[0, 0] + image.image_extent[1],
            transformed_positions[0, 1] + image.image_extent[2],
            transformed_positions[0, 1] + image.image_extent[3],
        )
        axes_image.set_extent(transformed_extent)

    def __render_mesh(
        self,
        axes: matplotlib.axes.Axes,
        mesh: Mesh,
        full_uuid: str,
        camera: Camera,
    ) -> None:
        transform = camera.transform

        if full_uuid not in self._polyCollections:
            # print(f"Creating new PathCollection for mesh visual {full_uuid}")
            self._polyCollections[full_uuid] = matplotlib.collections.PolyCollection([], clip_on=False, snap=False)
            axes.add_collection(self._polyCollections[full_uuid], autolim=False)

        polyCollection = self._polyCollections[full_uuid]

        T = mpl3d.glm.transform(mesh.vertices, transform)[mesh.faces]
        Z = -T[:, :, 2].mean(axis=1)

        if mesh.cmap is not None:
            # Facecolors using depth buffer
            norm = matplotlib.colors.Normalize(vmin=Z.min(), vmax=Z.max())
            facecolors = mesh.cmap(norm(Z))
        else:
            facecolors = mesh.facecolors

        edgecolors = mesh.edgecolors
        linewidths = mesh.linewidths

        # Back face culling
        if mesh.mode == "front":
            front, back = mpl3d.glm.frontback(T)
            T, Z = T[front], Z[front]
            if len(facecolors) == len(mesh.faces):
                facecolors = facecolors[front]
            if len(edgecolors) == len(mesh.faces):
                edgecolors = edgecolors[front]

        # Front face culling
        elif mesh.mode == "back":
            front, back = mpl3d.glm.frontback(T)
            T, Z = T[back], Z[back]
            if len(facecolors) == len(mesh.faces):
                facecolors = facecolors[back]
            if len(edgecolors) == len(mesh.faces):
                edgecolors = edgecolors[back]

        # Separate 2d triangles from zbuffer
        triangles = T[:, :, :2]
        antialiased = linewidths > 0

        # Sort triangles according to z buffer
        I = np.argsort(Z)
        triangles = triangles[I, :]
        if len(facecolors) == len(I):
            facecolors = facecolors[I, :]
        if len(edgecolors) == len(I):
            edgecolors = edgecolors[I, :]

        polyCollection.set_verts(triangles)
        polyCollection.set_linewidth(linewidths)
        polyCollection.set_facecolor(facecolors)  # type: ignore
        polyCollection.set_edgecolor(edgecolors)  # type: ignore
        polyCollection.set_antialiased(antialiased)
