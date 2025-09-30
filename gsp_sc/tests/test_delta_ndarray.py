import numpy as np
from gsp_sc.tmp.delta_ndarray.delta_ndarray import DeltaNdarray


def test_delta_ndarray_setitem_and_delta_tracking() -> None:
    arr = DeltaNdarray(np.zeros((4, 4), dtype=int))
    assert arr.is_modified() is False
    arr[1, 2] = 7
    arr[2, 1] = 8
    assert arr.is_modified() is True
    slices = arr.get_delta_slices()
    assert slices == (slice(1, 3), slice(1, 3))
    delta = arr.get_delta()
    assert np.array_equal(delta, arr[1:3, 1:3])


def test_delta_ndarray_clear_delta() -> None:
    arr = DeltaNdarray(np.zeros((3, 3), dtype=int))
    arr[0, 0] = 1
    assert arr.get_delta_slices() == (slice(0, 1), slice(0, 1))
    arr.clear_delta()
    assert arr.is_modified() is False


def test_delta_ndarray_patch_and_json_serialization() -> None:
    arr = DeltaNdarray(np.zeros((2, 2), dtype=int))
    arr[0, 1] = 5
    json_dict = arr.to_json()
    assert json_dict["slices"] is not None
    arr2 = DeltaNdarray.from_json(json_dict, arr, in_place=False)
    assert np.array_equal(arr2, arr)
    arr3 = DeltaNdarray.from_json(json_dict, arr, in_place=True)
    assert np.array_equal(arr3, arr)
    assert arr3 is arr


def test_delta_ndarray_full_serialization_when_no_modifications() -> None:
    arr = DeltaNdarray(np.ones((2, 2), dtype=int))
    json_dict = arr.to_json()
    assert json_dict["slices"] is None
    arr2 = DeltaNdarray.from_json(json_dict, None)
    assert np.array_equal(arr2, arr)


def test_delta_ndarray_slice_to_json_and_from_json() -> None:
    slices = (slice(1, 3, 1), slice(0, 2, 1))
    json_slices = DeltaNdarray.slice_to_json(slices)
    restored_slices = DeltaNdarray.slice_from_json(json_slices)
    assert restored_slices == slices
