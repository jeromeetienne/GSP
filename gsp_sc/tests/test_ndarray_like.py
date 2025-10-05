from gsp_sc.src.types.ndarray_like import (
    NdarrayLikeSerializedType,
    NdarrayLikeVariableType,
)
from gsp_sc.src.types.ndarray_like import NdarrayLikeUtils
from gsp_sc.src.types.diffable_ndarray import DiffableNdarray
import numpy as np


def test_ndarray_like_to_json() -> None:
    ndarray_like: NdarrayLikeVariableType = DiffableNdarray(np.arange(9).reshape(3, 3))
    serialized = NdarrayLikeUtils.to_json(ndarray_like)
    assert "uuid" in serialized["data"], "UUID should be included in the serialized output"
    assert serialized["type"] == "delta_ndarray", "Type should be 'delta_ndarray'"
    assert isinstance(serialized["data"], dict), "Data should be a dictionary"


def test_ndarray_like_to_from_json() -> None:
    ndarray_like_src: NdarrayLikeVariableType = DiffableNdarray(np.arange(9).reshape(3, 3))

    # Serialize the original array
    serialized1 = NdarrayLikeUtils.to_json(ndarray_like_src)
    assert serialized1["type"] == "delta_ndarray", "Type should be 'delta_ndarray'"
    assert serialized1["data"]["slices"] == None, "Slices should be None for unmodified array"
    assert isinstance(serialized1["data"], dict), "Data should be a dictionary"

    # Deserialize the original array
    deserialized1 = NdarrayLikeUtils.from_json(serialized1)
    assert np.array_equal(deserialized1, ndarray_like_src), "Deserialized array should match the original"
    assert isinstance(deserialized1, DiffableNdarray), "Deserialized object should be a DiffableNdarray"
    assert deserialized1.get_uuid() != ndarray_like_src.get_uuid(), "UUIDs should not match after deserialization"

    # Modify the original array to create a diff
    ndarray_like_src[1, 1] = -10  # Modify the array to create a diff
    assert ndarray_like_src.is_modified() == True, "Array should be marked as modified"

    # Serialize the modified array
    serialized2 = NdarrayLikeUtils.to_json(ndarray_like_src)
    assert ndarray_like_src.is_modified() == False, "Array should be unmodified after serialization"
    assert serialized2["type"] == "delta_ndarray", "Type should be 'delta_ndarray'"
    assert serialized2["data"]["slices"] != None, "Slices should not be None for modified array"

    # Deserialize the modified array
    deserialized2 = NdarrayLikeUtils.from_json(serialized2)
    assert np.array_equal(deserialized2, ndarray_like_src), "Deserialized array should match the modified original"
    assert deserialized2.get_uuid() != ndarray_like_src.get_uuid(), "UUIDs should not match after deserialization"
    assert deserialized2.get_uuid() == deserialized1.get_uuid(), "UUIDs should match the first deserialized array"
