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
from ...transform import TransformOrNdarray
from .renderer import MatplotlibRenderer

class RendererPixels:
    @staticmethod
    def render(
        renderer: 'MatplotlibRenderer',
        axes: matplotlib.axes.Axes,
        pixels: Pixels,
        full_uuid: str,
        camera: Camera,
    ) -> None:
        # Notify pre-rendering event
        pixels.pre_rendering.send(renderer)

        if full_uuid in renderer._pathCollections:
            pathCollection = renderer._pathCollections[full_uuid]
        else:
            # print(f"Creating new PathCollection for pixels visual {full_uuid}")
            pathCollection = axes.scatter([], [])
            renderer._pathCollections[full_uuid] = pathCollection

        # compute positions
        pixels_positions = TransformOrNdarray.to_ndarray(pixels.positions)

        # apply camera transform to positions
        transformed_positions: np.ndarray = mpl3d.glm.transform(pixels_positions, camera.transform)

        # Notify post-transform event
        pixels.post_transform.send(
            renderer,
            **{
                "camera": camera,
                "transformed_positions": transformed_positions,
            },
        )

        pathCollection.set_offsets(transformed_positions)
        pathCollection.set_sizes(TransformOrNdarray.to_ndarray(pixels.sizes))
        pathCollection.set_color(TransformOrNdarray.to_ndarray(pixels.colors).tolist())
        # pathCollection.set_edgecolor([0,0,0,1])

        # Notify post-rendering event
        pixels.post_rendering.send()
