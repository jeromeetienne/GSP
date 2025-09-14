from ..core.visual_base import VisualBase

import numpy as np


class Image(VisualBase):
    __slots__ = ("position", "image_extent", "image_data")

    def __init__(
        self, 
        position: np.ndarray,
        image_extent: tuple[float, float, float, float],
        image_data: np.ndarray
    ) -> None:
        super().__init__()

        self.position = position
        self.image_data = image_data
        self.image_extent = image_extent
