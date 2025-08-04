import numpy as np

# define projection matrices
def frustum(left: float, right: float, bottom: float, top: float, znear: float, zfar: float) -> np.ndarray:
    """
    Create a perspective projection matrix.

    Args:
        left (float): The left vertical clipping plane.
        right (float): The right vertical clipping plane.
        bottom (float): The bottom horizontal clipping plane.
        top (float): The top horizontal clipping plane.
        znear (float): The near clipping plane.
        zfar (float): The far clipping plane.

    Returns:
        M (numpy.ndarray): A 4x4 perspective projection matrix.
    """
    M = np.zeros((4, 4), dtype=np.float32)
    M[0, 0] = +2.0 * znear / (right - left)
    M[1, 1] = +2.0 * znear / (top - bottom)
    M[2, 2] = -(zfar + znear) / (zfar - znear)
    M[0, 2] = (right + left) / (right - left)
    M[2, 1] = (top + bottom) / (top - bottom)
    M[2, 3] = -2.0 * znear * zfar / (zfar - znear)
    M[3, 2] = -1.0
    return M

def perspective(fovy: float, aspect: float, znear: float, zfar: float) -> np.ndarray:
    """
    Create a perspective projection matrix based on field of view, aspect ratio, and near/far planes.
    """
    h = np.tan(0.5*np.radians(fovy)) * znear
    w = h * aspect
    return frustum(-w, w, -h, h, znear, zfar)

