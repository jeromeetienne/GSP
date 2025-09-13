from .viewport import Viewport

import uuid

class Canvas:
    __slots__ = ("uuid", "width", "height", "dpi", "viewports")
    def __init__(self, width: int, height: int, dpi: float = 100.0) -> None:
        self.uuid = str(uuid.uuid4())
        self.width = width
        self.height = height
        self.dpi = dpi
        self.viewports: list[Viewport] = []

    def add(self, viewport: Viewport) -> None:
        """
        Add a viewport to the canvas.

        Args:
            viewport (Viewport): The viewport to add.
        """
        self.viewports.append(viewport)
