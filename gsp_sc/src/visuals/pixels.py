import numpy as np
import nptyping

from ..core.visual_base import VisualBase

class Pixels(VisualBase):
    __slots__ = ("positions", "sizes", "colors")

    def __init__(
        self,
        positions: nptyping.NDArray[nptyping.Shape["*, 3"], nptyping.Float],
        sizes: nptyping.NDArray[nptyping.Shape["*"], nptyping.Float] = np.array([5.0]),
        colors: tuple[float, float, float, float] = (0.0, 0.0, 1.0, 1.0),
    ) -> None:
        super().__init__()

        # sanity check - np.ndarray type checking at runtime
        assert positions.shape[1:] == (3,), "Positions must have shape (N, 3) where N is the number of positions."
        assert sizes.shape == (1,), "Sizes must have shape (N, 1) where N is the number of sizes."

        self.positions = positions
        self.sizes = sizes
        self.colors = colors
