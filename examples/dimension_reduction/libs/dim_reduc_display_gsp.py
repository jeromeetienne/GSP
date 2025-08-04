from gsp.matplotlib import core, visual, glm
from gsp.matplotlib import core, visual, glm
import matplotlib.pyplot as plt
import numpy as np

import gsp
gsp.use("matplotlib")

# define __dirname__ to the directory of this script
import os
__dirname__ = os.path.dirname(os.path.abspath(__file__))

def display_gsp_scatter_plot(points_fitted: np.ndarray, points_colors: np.ndarray, image_filename: str = None):

    # Normalize umap_points_fitted to -1 to 1 range for better visualization
    point_min = -0.25
    point_max = 0.25
    points_fitted = (points_fitted - points_fitted.min(axis=0)) / (points_fitted.max(axis=0) - points_fitted.min(axis=0)) * (point_max - point_min) + point_min


    canvas = core.Canvas(512, 512, 100.0)
    viewport = core.Viewport(canvas, 0, 0, 512, 512, [1,1,1,1])
    pixels = visual.Pixels(points_fitted, colors=points_colors)

    from libs.camera import Camera
    camera = Camera("ortho")
    camera.connect(viewport, "motion",  pixels.render)
    if image_filename is not None:
        camera.save(image_filename)
    camera.run()

