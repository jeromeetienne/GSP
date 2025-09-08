# Package: Graphic Server Protocol / Matplotlib
# Authors: Nicolas P .Rougier <nicolas.rougier@gmail.com>
# License: BSD 3 clause
# from __future__ import annotations
import numpy as np
from gsp import core
from gsp.core import Color
from gsp.transform import Transform
from . canvas import Canvas

class Texture(core.Texture):

    __doc__ = core.Texture.__doc__

    def __init__(self, texture_data: np.ndarray, shape: tuple[int, int, int, int]):

        super().__init__(texture_data=texture_data, shape=shape)

        self._texture_data = texture_data
        self._shape = shape

    @property
    def data(self) -> np.ndarray:
        return self._texture_data

    @property
    def shape(self) -> tuple[int, int, int, int]:
        return self._shape
    