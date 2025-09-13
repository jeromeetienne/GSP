import uuid

class VisualBase:
    __slots__ = ("uuid",)
    def __init__(self) -> None:
        self.uuid = str(uuid.uuid4())
