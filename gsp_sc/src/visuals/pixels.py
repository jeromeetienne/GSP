import numpy as np
import nptyping

from ..core.visual_base import VisualBase
from ..transform import TransformChain

class Pixels(VisualBase):
    __slots__ = ("positions", "sizes", "colors")

    def __init__(
        self,
        positions: nptyping.NDArray[nptyping.Shape["*, 3"], nptyping.Float] | TransformChain,
        sizes: nptyping.NDArray[nptyping.Shape["*"], nptyping.Float] = np.array([5.0]),
        colors: nptyping.NDArray[nptyping.Shape["*, 4"], nptyping.Float] = np.array([[0.0, 0.0, 1.0, 1.0]]),
    ) -> None:
        """
        Initialize a Pixels visual.
        
        :param positions: np.ndarray of shape (N, 3) representing the 3D positions of the pixels
        :type positions: nptyping.NDArray[nptyping.Shape["*, 3"], nptyping.Float]
        :param sizes: np.ndarray of shape (N,) representing the sizes of the pixels
        :type sizes: nptyping.NDArray[nptyping.Shape["*"], nptyping.Float]
        :param colors: np.ndarray of shape (4,) representing the RGBA color of the pixels
        :type colors: np.ndarray
        """
        super().__init__()

        # sanity check - np.ndarray type checking at runtime
        if type(positions) is np.ndarray:
            assert positions.shape[1:] == (3,), "Positions must have shape (N, 3) where N is the number of positions."
        assert sizes.shape.__len__() == 1, "Sizes must have shape (N, 1) where N is the number of sizes."
        assert colors.shape[1:] == (4,), "Colors must be a numpy array of shape (4,)"

        self.positions = positions
        self.sizes = sizes
        self.colors = colors
