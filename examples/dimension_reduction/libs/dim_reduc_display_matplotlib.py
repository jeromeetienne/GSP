import matplotlib.pyplot as plt
import numpy as np
import gsp as gsp
from gsp.matplotlib import core, visual, glm

def display_matplotlib_scatter_plot(points_fitted, points_colors):
    """
    Display a scatter plot of the fitted points with colors.

    Args:
        points_fitted (np.ndarray): The points after UMAP fitting.
        points_colors (np.ndarray): The colors corresponding to each point.
    """
    plt.scatter(points_fitted[:,0], points_fitted[:,1], c=points_colors, s=1)

def display_matplotlib_point_labels(points_fitted, labels_original):
    """
    Display labels on the fitted plot at the center of each cluster.

    Args:
        points_fitted (np.ndarray): The points after UMAP fitting.
        labels_original (np.ndarray): The original labels for each point.
    """

    for label in range(len(np.unique(labels_original))):
        print(f"Computing center for label {label}")
        label_indices = np.where(labels_original == label)[0]
        label_points = points_fitted[label_indices]
        label_center = np.mean(label_points, axis=0)
        plt.text(label_center[0], label_center[1], str(label), fontsize=12, ha='center', va='center')

def display_gsp_pixels(points_fitted, points_colors, canvas_width=1024, canvas_height=1024):

    # Create a canvas and viewport
    canvas = gsp.core.Canvas(canvas_width, canvas_height, 100.0)
    viewport = gsp.core.Viewport(canvas, 0, 0, canvas_width, canvas_height, [1,1,1,1])

    # Create a Pixels visual
    # pixels = visual.Pixels(points_fitted_3d, colors=gsp.black)
    # pixels = gsp.visual.Pixels(points_fitted_3d, colors=points_colors)


    # Create a Pixels visual
    pixels = visual.Pixels(points_fitted, colors=gsp.black)
    # pixels = visual.Pixels(points_fitted, colors=points_colors)

    # display in points
    # sizes = glm.float(len(point_positions))
    # sizes[...] = 40
    # pixels = visual.Points(point_positions, sizes, gsp.grey, gsp.black, [0.5])
    # pixels = visual.Points(point_positions, sizes, point_colors, gsp.black, [0])

    from .camera import Camera
    camera = Camera("ortho")
    camera.connect(viewport, "motion",  pixels.render)
    camera.run()
    # # Connect the camera to the viewport
    # camera = Camera("perspective", theta=-30, phi=0, log_fps_enabled=True, scale=5.0)

    # camera.connect(viewport, "motion", pixels.render)

    # # Render the pixels visual
    # print('Rendering pixels visual...')
    # camera.run()


