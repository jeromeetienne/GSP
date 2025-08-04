from gsp.matplotlib import core, visual, glm
from gsp.matplotlib import core, visual, glm
import matplotlib.pyplot as plt
import numpy as np

import gsp
gsp.use("matplotlib")

# define __dirname__ to the directory of this script
import os
__dirname__ = os.path.dirname(os.path.abspath(__file__))

def display_gsp_scatter_plot(points_fitted: np.ndarray, points_colors: np.ndarray):

    canvas = core.Canvas(512, 512, 100.0)
    viewport = core.Viewport(canvas, 0, 0, 512, 512, [1,1,1,1])
    pixels = visual.Pixels(points_fitted, colors=points_colors)

    from libs.camera import Camera
    camera = Camera("ortho")
    camera.connect(viewport, "motion",  pixels.render)
    camera.save(f"{__dirname__}/../../output/dim_reduc_umap_mnist.png")
    camera.run()

