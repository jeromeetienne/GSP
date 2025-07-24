import numpy as np

def translate(x: float, y: float, z: float) -> np.ndarray:
    """
    Create a translation matrix.

    Args:
        x (float): Translation along the x-axis.
        y (float): Translation along the y-axis.
        z (float): Translation along the z-axis.

    Returns:
        M (numpy.ndarray): A 4x4 translation matrix.
    """
    return np.array([[1, 0, 0, x], [0, 1, 0, y],
                     [0, 0, 1, z], [0, 0, 0, 1]], dtype=float)

def xrotate(theta: float) -> np.ndarray:
    """
    Create a rotation matrix around the x-axis.

    Args:
        theta (float): The angle of rotation in degrees.

    Returns:
        M (numpy.ndarray): A 4x4 rotation matrix.
    """
    t = np.pi * theta / 180
    c, s = np.cos(t), np.sin(t)
    return np.array([[1, 0,  0, 0], [0, c, -s, 0],
                     [0, s,  c, 0], [0, 0,  0, 1]], dtype=float)

def yrotate(theta: float) -> np.ndarray:
    """
    Create a rotation matrix around the y-axis.

    Returns:
        M (numpy.ndarray): A 4x4 rotation matrix.
    """
    t = np.pi * theta / 180
    c, s = np.cos(t), np.sin(t)
    return  np.array([[ c, 0, s, 0], [ 0, 1, 0, 0],
                      [-s, 0, c, 0], [ 0, 0, 0, 1]], dtype=float)
