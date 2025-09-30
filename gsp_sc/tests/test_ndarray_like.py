# pip imports
import numpy as np
import pytest

# local imports
from gsp_sc.tmp.delta_ndarray.ndarray_like import NdarrayLikeUtils
from gsp_sc.tmp.delta_ndarray.delta_ndarray import DeltaNdarray
from gsp_sc.src.transform import TransformLinkImmediate, TransformLinkLambda, TransformSerialisation
from gsp_sc.src.transform.transform_link_base import TransformLinkBase

def test_to_json_and_from_json_with_ndarray():
    arr = np.array([[1, 2], [3, 4]])
    serialized = NdarrayLikeUtils.to_json(arr)
    assert serialized["type"] == "ndarray"
    assert serialized["data"] == [[1, 2], [3, 4]]

    deserialized = NdarrayLikeUtils.from_json(serialized)
    np.testing.assert_array_equal(deserialized, arr) # type: ignore

def test_to_json_and_from_json_with_delta_ndarray():
    arr = [[5, 6], [7, 8]]
    delta = DeltaNdarray(arr)
    serialized = NdarrayLikeUtils.to_json(delta)
    assert serialized["type"] == "delta_ndarray"
    assert isinstance(serialized["data"], dict)

    # DeltaNdarray.from_json expects previous_ndarray_like, but for initial, None is allowed
    deserialized = NdarrayLikeUtils.from_json(serialized, previous_ndarray_like=None)
    assert isinstance(deserialized, DeltaNdarray)
    np.testing.assert_array_equal(deserialized, np.array(arr))

def test_to_json_and_from_json_with_transform_link_base():
    arr = np.array([[1, 2], [3, 4]])
    link = TransformLinkImmediate(arr).chain(TransformLinkLambda(lambda x: x + 1))
    serialized = NdarrayLikeUtils.to_json(link)
    assert serialized["type"] == "transform_links"
    assert isinstance(serialized["data"], list)

    deserialized = NdarrayLikeUtils.from_json(serialized)
    assert isinstance(deserialized, TransformLinkBase)
    np.testing.assert_array_equal(deserialized.run(), arr + 1)

def test_to_ndarray_with_ndarray():
    arr = np.array([1, 2, 3])
    result = NdarrayLikeUtils.to_ndarray(arr)
    np.testing.assert_array_equal(result, arr)

def test_to_ndarray_with_transform_link_base():
    arr = np.array([1, 2, 3])
    link = TransformLinkImmediate(arr).chain(TransformLinkLambda(lambda x: x * 2))
    result = NdarrayLikeUtils.to_ndarray(link)
    np.testing.assert_array_equal(result, arr * 2)

def test_to_ndarray_with_delta_ndarray():
    arr = [[9, 8], [7, 6]]
    delta = DeltaNdarray(arr)
    result = NdarrayLikeUtils.to_ndarray(delta)
    np.testing.assert_array_equal(result, np.array(arr))

def test_to_json_invalid_type():
    class Dummy: pass
    with pytest.raises(TypeError):
        NdarrayLikeUtils.to_json(Dummy()) # type: ignore

def test_from_json_invalid_type():
    with pytest.raises(TypeError):
        NdarrayLikeUtils.from_json({"type": "unknown", "data": 123})

def test_from_json_ndarray_data_not_list():
    with pytest.raises(TypeError):
        NdarrayLikeUtils.from_json({"type": "ndarray", "data": "not_a_list"})

def test_from_json_delta_ndarray_requires_previous():
    arr = [[1, 2], [3, 4]]
    delta = DeltaNdarray(arr)
    serialized = NdarrayLikeUtils.to_json(delta)
    # previous_ndarray_like must be DeltaNdarray or None, so passing wrong type should assert
    with pytest.raises(AssertionError):
        NdarrayLikeUtils.from_json(serialized, previous_ndarray_like=np.array(arr))