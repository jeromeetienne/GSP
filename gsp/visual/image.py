# Package: Graphic Server Protocol
# Authors: Nicolas P .Rougier <nicolas.rougier@gmail.com>
# License: BSD 3 clause

import numpy as np
from gsp import glm
from gsp.visual import Visual
from gsp.core import Buffer, Color
from gsp.transform import Transform
from gsp.io.command import command


class Image(Visual):
    """
    TODO to write
    """

    @command("visual.Image")
    def __init__(
        self, positions: Transform | Buffer, image_data: np.ndarray, image_extent: tuple
    ):
        """
        TODO to write
        """

        super().__init__()

        # These variables are available prior to rendering
        self._in_variables = {
            "positions": positions,
            "image_data": image_data,
            "image_extent": image_extent,
            "viewport": None,
        }

        # These variables exists only during rendering and are
        # available on server side only. We have thus to make
        # sure they are not tracked.
        n = len(positions)
        self._out_variables = {
            "screen[positions]": np.empty((n, 3), np.float32),
        }
