from ..core.visual_base import VisualBase

import numpy as np

class Pixels(VisualBase):
    def __init__(self, positions: np.ndarray, sizes: np.ndarray, colors: tuple[float,float,float,float]):
        super().__init__()

        self.positions = positions
        self.sizes = sizes
        self.colors = colors

    
