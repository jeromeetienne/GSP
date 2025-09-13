from ..core.visual_base import VisualBase

import numpy as np


class Image(VisualBase):
    __slots__ = ("bounds", "image_data")

    def __init__(
        self, bounds: tuple[float, float, float, float], image_data: np.ndarray
    ) -> None:
        super().__init__()

        self.image_data = image_data
        self.bounds = bounds
