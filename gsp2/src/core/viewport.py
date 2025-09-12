from .visual_base import VisualBase

class Viewport:
    def __init__(self,  x: int, y: int, width: int, height: int, background_color: tuple[float, float, float, float]=(1,1,1, 1)):
        """
        Initialize a viewport.

        Args:
            x (int): The x position of the viewport in the Canvas.
            y (int): The y position of the viewport in the Canvas.
            width (int): The width of the viewport in the Canvas.
            height (int): The height of the viewport in the Canvas.
            background_color (tuple[float, float, float, float]): The background color of the viewport.
        """
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.background_color = background_color

        self.visuals: list[VisualBase] = []

    def add(self, visual: VisualBase) -> None:
        """
        Add a visual to the viewport.

        Args:
            visual (VisualBase): The visual to add.
        """
        self.visuals.append(visual)
