from .viewport import Viewport

class Canvas:
    __slots__ = ("width", "height", "dpi", "viewports")
    def __init__(self, width: int, height: int, dpi: float = 100.0):
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
