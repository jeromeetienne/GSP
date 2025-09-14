import uuid
import mpl3d.camera
from .canvas import Canvas

from gsp_sc.src.renderer.matplotlib import renderer

class Camera:
    def __init__(self, mode: str = "perspective"):
        self._mpl3d_camera = mpl3d.camera.Camera("perspective")

    def run(self, canvas: gsp_sc.core.Canvas) -> None:
        def camera_update(transform) -> None:
            renderer.render(canvas, transform_matrix=transform, show_image=False)

import matplotlib.pyplot as plt
mpl3d_camera = mpl3d.camera.Camera("perspective")
renderer.render(canvas, transform_matrix=mpl3d_camera.transform, show_image=False)

figure = plt.gcf()
mpl_axes = figure.get_axes()[0]
mpl3d_camera.connect(mpl_axes, camera_update)

plt.show(block=True)

