# stdlib imports
import typing
from typing import Any

# pip imports
import numpy as np

# local imports
from gsp_sc.src.transform import TransformSerialisation
from gsp_sc.src.transform.transform_link_base import TransformLinkBase
from gsp_sc.src.transform import TransformLinkImmediate, TransformLinkLambda
from gsp_sc.src.diffable_ndarray.diffable_ndarray import DiffableNdarray
from gsp_sc.src.diffable_ndarray.diffable_ndarray_serialisation import DiffableNdarraySerialisation

NdarrayLikeVariableType = TransformLinkBase | DiffableNdarray | np.ndarray

NdarrayLikeSerializedType = dict[str, Any]


class NdarrayLikeUtils:
    """
    Utility class to handle inputs that can be either a numpy ndarray or a TransformLinkBase chain or a DeltaNdarray.
    This class provides methods to serialize/deserialize them to/from JSON-compatible formats.


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
            delta_array = typing.cast(DiffableNdarray, data)
            serialized_dict = {"type": "delta_ndarray", "data": DiffableNdarraySerialisation.to_json(delta_array)}
            return serialized_dict
        elif isinstance(data, np.ndarray):
            ndarray = typing.cast(np.ndarray, data)
            serialized_dict = {"type": "ndarray", "data": ndarray.tolist()}
            return serialized_dict
        else:
            raise TypeError("Input must be either a numpy ndarray or a TransformLinkBase instance.")

    @staticmethod
    def from_json(serialized_data: NdarrayLikeSerializedType, previous_ndarray_like: NdarrayLikeVariableType | None = None) -> NdarrayLikeVariableType:
        """
        Convert a JSON-serializable format to either a TransformLinkBase or a numpy ndarray.

        arguments:
            serialized_data: The JSON-serializable dictionary.
            previous_ndarray_like: Optional previous NdarrayLikeVariableType, required if serialized_data is of type DeltaNdarray
        """

        if serialized_data["type"] == "transform_links":
            json_array = typing.cast(list[dict[str, Any]], serialized_data["data"])
            link_head = TransformSerialisation.from_json(json_array)
            return link_head
        elif serialized_data["type"] == "delta_ndarray":
            assert isinstance(previous_ndarray_like, DiffableNdarray | None), "previous_ndarray_like must be DeltaNdarray or None"
            delta_array = DiffableNdarraySerialisation.from_json(serialized_data["data"], previous_ndarray_like)
            return delta_array
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
#
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
