from .visual_base import VisualBase

class Viewport:
    def __init__(self,  x: int, y: int, width: int, height: int, background_color: tuple[float, float, float, float]=(1,1,1, 1)):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.background_color = background_color

        self.visuals: list[VisualBase] = []

    def add_visual(self, visual: VisualBase) -> None:
        self.visuals.append(visual)
