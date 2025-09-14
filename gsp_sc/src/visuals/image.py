import numpy as np
import nptyping

from ..core.visual_base import VisualBase

class Image(VisualBase):
    __slots__ = ("position", "image_extent", "image_data")

    def __init__(
        self, 
        position: nptyping.NDArray[nptyping.Shape["1, 3"], nptyping.Float],
        image_extent: tuple[float, float, float, float],
        image_data: np.ndarray
    ) -> None:
        super().__init__()

        self.position = position
        self.image_data = image_data
        self.image_extent = image_extent
