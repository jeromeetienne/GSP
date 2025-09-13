from .visual_base import VisualBase

import uuid

class Viewport:
    __slots__ = (
        "uuid",
        "origin_x",
        "origin_y",
        "width",
        "height",
        "background_color",
        "visuals",
    )

    def __init__(
        self,
        origin_x: int,
        origin_y: int,
        width: int,
        height: int,
        background_color: tuple[float, float, float, float] = (1, 1, 1, 1),
    ) -> None:
        """
        Initialize a viewport.

        Args:
            origin_x (int): The x position of the viewport in the Canvas.
            origin_y (int): The y position of the viewport in the Canvas.
            width (int): The width of the viewport in the Canvas.
            height (int): The height of the viewport in the Canvas.
            background_color (tuple[float, float, float, float]): The background color of the viewport.
        """
        self.uuid = str(uuid.uuid4())
        self.origin_x = origin_x
        self.origin_y = origin_y
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
