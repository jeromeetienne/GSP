# stdlib imports
import typing
from typing import Any

# pip imports
import numpy as np

# local imports
from ..transform import TransformSerialisation
from ..transform.transform_link_base import TransformLinkBase
from ..transform import TransformLinkImmediate, TransformLinkLambda
from .diffable_ndarray.diffable_ndarray import DiffableNdarray
from .diffable_ndarray.diffable_ndarray_serialisation import DiffableNdarraySerialisation

NdarrayLikeVariableType = TransformLinkBase | DiffableNdarray | np.ndarray

NdarrayLikeSerializedType = dict[str, Any]


from_json_diffable_ndarray_db: dict[str, DiffableNdarray] = {}
"""A simple in-memory database to store DiffableNdarray instances by their UUIDs during deserialization."""


class NdarrayLikeUtils:
    """
    Utility class to handle inputs that can be either a numpy ndarray or a TransformLinkBase chain or a DeltaNdarray.
    This class provides methods to serialize/deserialize them to/from JSON-compatible formats.

    NOTE: once you sent a DiffableNdarray through to_json, its diff tracking is cleared.
    """

    @staticmethod
    def to_json(data: NdarrayLikeVariableType) -> NdarrayLikeSerializedType:
        """
        Convert the input data to a JSON-serializable format.
        """
        if isinstance(data, TransformLinkBase):
            link_head = typing.cast(TransformLinkBase, data)
            serialized_dict = {"type": "transform_links", "data": TransformSerialisation.to_json(link_head)}
            return serialized_dict
        elif isinstance(data, DiffableNdarray):
            diffable_array = typing.cast(DiffableNdarray, data)
            serialized_dict = {"type": "delta_ndarray", "data": DiffableNdarraySerialisation.to_json(diffable_array, diff_allowed=True)}
            diffable_array.clear_diff()  # Clear the diff tracking after serialization
            return serialized_dict
        elif isinstance(data, np.ndarray):
            ndarray = typing.cast(np.ndarray, data)
            serialized_dict = {"type": "ndarray", "data": ndarray.tolist()}
            return serialized_dict
        else:
            raise TypeError("Input must be either a numpy ndarray or a TransformLinkBase instance.")

    @staticmethod
    def from_json(serialized_data: NdarrayLikeSerializedType, diffable_ndarray_db=from_json_diffable_ndarray_db) -> NdarrayLikeVariableType:
        """
        Convert a JSON-serializable format to either a TransformLinkBase or a numpy ndarray.

        Arguments:
            serialized_data (NdarrayLikeSerializedType): The JSON-serializable dictionary.
        """

        if serialized_data["type"] == "transform_links":
            json_array = typing.cast(list[dict[str, Any]], serialized_data["data"])
            link_head = TransformSerialisation.from_json(json_array)
            return link_head
        elif serialized_data["type"] == "delta_ndarray":
            # 1. try to get a previous ndarray with the same uuid in our database
            serialized_uuid = serialized_data["data"]["uuid"]
            previous_diffable_array = diffable_ndarray_db[serialized_uuid] if serialized_uuid in diffable_ndarray_db else None
            # 2. create a new delta_array from the serialized data and the previous one
            new_diffable_array = DiffableNdarraySerialisation.from_json(serialized_data["data"], previous_diffable_array, in_place=True)
            # 3. update the database with the new diffable_array and return it
            diffable_ndarray_db[serialized_uuid] = new_diffable_array
            # 4. return the new diffable_array
            return new_diffable_array
        elif serialized_data["type"] == "ndarray":
            if not isinstance(serialized_data["data"], list):
                raise TypeError("Expected 'data' to be a list.")
            array_np = np.array(serialized_data["data"])
            return array_np
        else:
            raise TypeError("Input list elements must be either dicts or numeric types.")

    @staticmethod
    def to_numpy(data: np.ndarray | TransformLinkBase | DiffableNdarray) -> np.ndarray:
        """
        Convert the input data to a numpy ndarray.
        """

        if isinstance(data, TransformLinkBase):
            link_head = typing.cast(TransformLinkBase, data)
            array_np = link_head.run()
            return array_np
        elif isinstance(data, np.ndarray):
            array_np = typing.cast(np.ndarray, data)
            return array_np
        elif isinstance(data, DiffableNdarray):
            delta_array = typing.cast(DiffableNdarray, data)
            return delta_array
        else:
            raise TypeError("Input must be either a numpy ndarray or a TransformLinkBase instance.")


###############################################################################
#   Example usage
# deserialized2
if __name__ == "__main__":
    # Example 1: Using a numpy ndarray
    arr = np.array([[1, 2, 3], [4, 5, 6]])
    assert isinstance(arr, NdarrayLikeVariableType), "np.ndarray should be a valid NdarrayLikeVariableType"
    serialized_arr = NdarrayLikeUtils.to_json(arr)
    print("Serialized ndarray:", serialized_arr)
    deserialized_arr = NdarrayLikeUtils.from_json(serialized_arr)
    print("Deserialized ndarray:", deserialized_arr)

    # Example 2: Using DeltaNdarray
    delta = DiffableNdarray([[10, 20], [30, 40]])
    assert isinstance(delta, NdarrayLikeVariableType), "DeltaNdarray should be a valid NdarrayLikeVariableType"
    serialized_delta = NdarrayLikeUtils.to_json(delta)
    print("Serialized DeltaNdarray:", serialized_delta)
    deserialized_delta = NdarrayLikeUtils.from_json(serialized_delta)
    print("Deserialized DeltaNdarray:", deserialized_delta)

    # Example 3: Using TransformLinkBase chain
    transformLinks = TransformLinkImmediate(np.array([[1, 2, 3], [4, 5, 6]])).chain(TransformLinkLambda(lambda x: x * 10))
    assert isinstance(transformLinks, NdarrayLikeVariableType), "TransformLinkBase should be a valid NdarrayLikeVariableType"
    serialized_transform = NdarrayLikeUtils.to_json(transformLinks)
    print("Serialized TransformLinkBase:", serialized_transform)
    deserialized_transform = typing.cast(TransformLinkBase, NdarrayLikeUtils.from_json(serialized_transform))
    print("Deserialized TransformLinkBase run result:", deserialized_transform.run())
