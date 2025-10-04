import numpy as np
from gsp_sc.tmp.delta_ndarray.delta_ndarray import DeltaNdarray
from gsp_sc.tmp.delta_ndarray.delta_ndarray_serialisation import DeltaNdarraySerialisation

def test_delta_ndarray_serialisation_no_modifications() -> None:
    # Create a DeltaNdarray with a 4x4 array of values 0..15
    arr = DeltaNdarray(np.arange(16).reshape(4, 4))
    
    # Serialize the DeltaNdarray to JSON with diff_allowed=True
    json_dict = DeltaNdarraySerialisation.to_json(arr, diff_allowed=True)
    
    # Assert that no slices (no modifications) are present in the serialization
    assert json_dict["slices"] is None
    
    # Assert that the serialized data matches the original array's list representation
    assert json_dict["data"] == arr.tolist()

    # Deserialize the JSON back into a DeltaNdarray
    new_arr = DeltaNdarraySerialisation.from_json(json_dict, previous_arr=None)
    
    # Assert that the deserialized array matches the original array
    assert np.array_equal(new_arr, arr)
    
    # Assert that the new array is not marked as modified
    assert new_arr.is_modified() is False

def test_delta_ndarray_serialisation_with_modifications_without_previous_arr() -> None:
    # Create a DeltaNdarray with a 4x4 array of values 0..15
    arr = DeltaNdarray(np.arange(16).reshape(4, 4))
    
    # Modify some elements in the array
    arr[1, 2] = -7
    arr[2, 1] = -8
    
    # Serialize the DeltaNdarray to JSON with diff_allowed=True
    json_dict = DeltaNdarraySerialisation.to_json(arr, diff_allowed=True)
    
    # Assert that slices (modifications) are present in the serialization
    assert json_dict["slices"] is not None
    
    # Assert that the serialized data matches the modified region of the array
    delta_slices = arr.get_delta_slices()
    assert json_dict["slices"] == DeltaNdarraySerialisation._slice_to_json(delta_slices)

    # Assert that the serialized data matches the modified region of the array
    delta_data = arr.get_delta_data()
    assert json_dict["data"] == delta_data.tolist()
    
    # Deserialize the JSON back into a DeltaNdarray using the original array as previous_arr
    new_arr = DeltaNdarraySerialisation.from_json(json_dict, previous_arr=arr)
    
    # Assert that the deserialized array matches the modified original array
    assert np.array_equal(new_arr, arr)
    
    # Assert that the new array is marked as modified
    assert new_arr.is_modified() is True

def test_delta_ndarray_serialisation_with_modifications_with_previous_arr() -> None:
    # Create a DeltaNdarray with a 4x4 array of values 0..15
    arr = DeltaNdarray(np.arange(16).reshape(4, 4))
    
    # Modify some elements in the array
    arr[1, 2] = -7
    arr[2, 1] = -8
    
    # Serialize the DeltaNdarray to JSON with diff_allowed=True
    json_dict = DeltaNdarraySerialisation.to_json(arr, diff_allowed=True)
    
    # Assert that slices (modifications) are present in the serialization
    assert json_dict["slices"] is not None
    
    # Assert that the serialized data matches the modified region of the array
    delta_slices = arr.get_delta_slices()
    assert json_dict["slices"] == DeltaNdarraySerialisation._slice_to_json(delta_slices)

    # Assert that the serialized data matches the modified region of the array
    delta_data = arr.get_delta_data()
    assert json_dict["data"] == delta_data.tolist()
    
    # Create a previous array identical to the original unmodified array
    previous_arr = DeltaNdarray(np.arange(16).reshape(4, 4))
    
    # Deserialize the JSON back into a DeltaNdarray using previous_arr
    new_arr = DeltaNdarraySerialisation.from_json(json_dict, previous_arr=previous_arr)
    
    # Assert that the deserialized array matches the modified original array
    assert np.array_equal(new_arr, arr)
    
    # Assert that the new array is marked as modified
    assert new_arr.is_modified() is True