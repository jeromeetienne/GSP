from .transform_link_base import TransformLinkBase

class TransformLinkDB():
    _database: dict[str, type['TransformLinkBase']] = {}

    @staticmethod
    def add_link(name: str, transform_class: type['TransformLinkBase']) -> None:
        """
        Register a transformation class with a name.
        """
        TransformLinkDB._database[name] = transform_class

    @staticmethod
    def get_link(name: str) -> type['TransformLinkBase']:
        """
        Retrieve a transformation class by name.
        """
        if name not in TransformLinkDB._database:
            raise ValueError(f"Transform '{name}' not found in the database.")
        return TransformLinkDB._database[name]