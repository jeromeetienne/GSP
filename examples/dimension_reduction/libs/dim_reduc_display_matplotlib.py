import matplotlib.pyplot as plt
import numpy as np
import gsp as gsp
from gsp.matplotlib import core, visual, glm

def display_matplotlib_scatter_plot(points_fitted: np.ndarray, points_colors: np.ndarray):
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
