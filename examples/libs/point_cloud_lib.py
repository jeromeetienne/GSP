# Experiment to handle intellisense in VSCode
from gsp.matplotlib import core, visual, glm
import matplotlib.pyplot as plt
import numpy as np

def load_lidar(point_cloud_npz_filename: str) -> tuple[np.ndarray, np.ndarray]:
    """
    Load the LIDAR data from a .npz file.

    Args:
        point_cloud_npz_filename (str): Path to the .npz file containing the LIDAR data. e.g. lidar.npz

    Returns:
        tuple: A tuple containing:
            - point_positions (np.ndarray): An array of shape (N, 3) containing the 3D positions of the points.
            - point_colors (np.ndarray): An array of shape (N, 4) containing the RGBA colors of the points, normalized to [0, 1].
    """


    # Load the LIDAR data
    point_cloud_data = np.load(point_cloud_npz_filename)
    point_positions, point_colors = point_cloud_data['pos'], point_cloud_data['color']

    # Normalize colors
    point_colors = point_colors / 255.0

    return point_positions, point_colors

def print_geometry_info(point_positions: np.ndarray):
    """ Print the point cloud information """
    print(f'Point cloud size: {len(point_positions)} points')
    print(f'Point positions shape: {point_positions.shape}')
    print(f'Point positions min: {point_positions.min(axis=0)}')
    print(f'Point positions max: {point_positions.max(axis=0)}')

def geometry_crop(
    point_positions: np.ndarray, point_colors: np.ndarray,
    x_min: float = None, x_max: float = None, y_min: float = None, y_max: float = None, z_min: float = None, z_max: float = None
) -> tuple[np.ndarray, np.ndarray]:
    """
    Crop the point cloud to a specific range.

    Args:
        point_positions (np.ndarray): The 3D positions of the points.
        point_colors (np.ndarray): The colors of the points.
        x_min (float, optional): Minimum x value.
        x_max (float, optional): Maximum x value.
        y_min (float, optional): Minimum y value.
        y_max (float, optional): Maximum y value.
        z_min (float, optional): Minimum z value.
        z_max (float, optional): Maximum z value.

    Returns:
        tuple: Cropped point positions and colors.
    """
    # Set defaults if not provided
    if x_min is None:
        x_min = point_positions[:, 0].min()
    if x_max is None:
        x_max = point_positions[:, 0].max()
    if y_min is None:
        y_min = point_positions[:, 1].min()
    if y_max is None:
        y_max = point_positions[:, 1].max()
    if z_min is None:
        z_min = point_positions[:, 2].min()
    if z_max is None:
        z_max = point_positions[:, 2].max()

    mask = (point_positions[:, 0] > x_min) & (point_positions[:, 0] < x_max) & \
           (point_positions[:, 1] > y_min) & (point_positions[:, 1] < y_max) & \
           (point_positions[:, 2] > z_min) & (point_positions[:, 2] < z_max)
    return point_positions[mask], point_colors[mask]
