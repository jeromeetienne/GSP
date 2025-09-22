import uuid
import blinker

class VisualBase:
    __slots__ = ("uuid")

    def __init__(self) -> None:
        self.uuid = str(uuid.uuid4())
        """
        The unique identifier of the visual.

        - Used in renderers to track visuals context across multiple render calls.
        """
