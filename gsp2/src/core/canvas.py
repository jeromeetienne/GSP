from .viewport import Viewport

class Canvas:
    def __init__(self, width: int, height: int, dpi: float = 100.0):
        self.width = width
        self.height = height
        self.dpi = dpi
        self.viewports: list[Viewport] = []

    def add_viewport(self, viewport: Viewport) -> None:
        self.viewports.append(viewport)
