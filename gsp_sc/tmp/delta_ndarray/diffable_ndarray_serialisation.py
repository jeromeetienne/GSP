from dataclasses import dataclass
from re import split
from tracemalloc import start
from typing import Any
import numpy as np
from gsp_sc.tmp.delta_ndarray.diffable_ndarray import DiffableNdarray
from dataclasses import dataclass

# TODO to rename DiffableNdarray ?
class DiffableNdarraySerialisation:
    ###############################################################################
    #   JSON serialisation
    #

    @staticmethod
    def to_json(diff_ndarray: DiffableNdarray, diff_allowed: bool = False) -> dict[str, Any]:
        """
        Serialize the DeltaNdarray to a JSON-serializable dictionary.
        """

        # No modifications, serialize the whole array
        if diff_allowed == False or diff_ndarray.is_modified() is False:
            json_dict = {
                "slices": None,
                "data": diff_ndarray.tolist(),
            }
            return json_dict

        # There are modifications, serialize only the delta region
        diff_slices = DiffableNdarray.get_diff_slices(diff_ndarray)
        diff_data = DiffableNdarray.get_diff_data(diff_ndarray)

        # Ensure the delta_region is valid
        assert diff_data is not None, "Delta region should not be None if delta slices exists"

        # Convert slices and data to a JSON-serializable format
        diff_slices_dict = DiffableNdarraySerialisation._slice_to_json(diff_slices)
        diff_data_dict = diff_data.tolist()

        # Serialize the slices and the delta region
        json_dict = {
            "slices": diff_slices_dict,
            "data": diff_data_dict,
        }
        return json_dict

    @staticmethod
    def from_json(json_dict: dict[str, Any], previous_arr: "DiffableNdarray|None", in_place: bool = False) -> "DiffableNdarray":
        """
        Deserialize a JSON-serializable dictionary back to a DeltaNdarray.
        """

        # No modifications, create a new DeltaNdarray with the full data
        if json_dict["slices"] is None:
            new_arr = DiffableNdarray(np.array(json_dict["data"]))
            return new_arr

        # from here, there are modifications to apply, so we need the previous array
        assert previous_arr is not None, "previous_arr must be provided if there are modifications to apply"

        # honor the in_place flag
        new_arr = previous_arr.copy() if not in_place else previous_arr

        # deserialize the slices and the delta region
        diff_slices = DiffableNdarraySerialisation._slice_from_json(json_dict["slices"])
        diff_data = np.array(json_dict["data"])

        # apply the patch
        new_arr.apply_patch(diff_slices, diff_data)

        return new_arr

    ###############################################################################
    #   Slice to/from JSON
    #
    @staticmethod
    def _slice_to_json(slices: tuple[slice, ...]) -> dict[str, Any]:
        """
        Convert a tuple of slices to a JSON-serializable dictionary.
        """
        slice_dict = {
            "slices": []
        }
        for _slice in slices:
            assert _slice.step in (None, 1), "Only slices with step=1 or step=None are supported"
            slice_dict["slices"].append({
                "start": _slice.start,
                "stop": _slice.stop,
            })
        return slice_dict

    @staticmethod
    def _slice_from_json(slice_dict: dict[str, Any]) -> tuple[slice, ...]:
        """
        Convert a JSON-serializable dictionary back to a tuple of slices.
        """
        slices_arr = [slice(_slice["start"], _slice["stop"], None) for _slice in slice_dict["slices"]]
        slices_tuple = tuple(slices_arr)
        return slices_tuple


###############################################################################
#   Example usage
#
if __name__ == "__main__":
    ###############################################################################
    #   Example usage without modifications - client side
    #
    delta_arr_client = DiffableNdarray(np.arange(25).reshape(5, 5))
    print("*" * 80)
    print("Initial array:\n", delta_arr_client)
    print("Is modified:", delta_arr_client.is_modified())

    delta_arr_client_dict = DiffableNdarraySerialisation.to_json(delta_arr_client)

    ###############################################################################
    #   Example usage without modifications - server side
    #

    delta_arr_server = None
    delta_arr_server = DiffableNdarraySerialisation.from_json(delta_arr_client_dict, delta_arr_server)

    # check delta_arr_client and delta_arr_server are identical
    assert np.array_equal(
        delta_arr_client, delta_arr_server
    ), "after deserialization of unchanged data, delta_arr_client and delta_arr_server are not identical"
    print("Initial array and deserialized array are identical")

    ###############################################################################
    #   Example usage with modifications - client side
    #
    print("*" * 80)

    print("MODIFYING ARRAY " + "*" * 80)
    delta_arr_client[1, 2] = -50
    delta_arr_client[3:5, 1:4] = -60
    print("Is modified:", delta_arr_client.is_modified())
    print("Delta slice:", delta_arr_client.get_diff_slices())
    print("Delta region:\n", delta_arr_client.get_diff_data())
    print("Modified array:\n", delta_arr_client)

    # Serialize to JSON
    delta_arr_json_dict = DiffableNdarraySerialisation.to_json(delta_arr_client)
    # Clear delta in client array after serialisation
    delta_arr_client.clear_diff()
    print("\nAfter serialisation and clearing delta: is_modified=", delta_arr_client.is_modified())

    ###############################################################################
    #   Example usage with modifications - server side
    #
    # Deserialize from JSON
    delta_arr_server = DiffableNdarraySerialisation.from_json(delta_arr_json_dict, delta_arr_server)
    print("\nDeserialized array:\n", delta_arr_server)
    print("Is modified:", delta_arr_server.is_modified())
    # check delta_arr_client and delta_arr_server are identical
    assert np.array_equal(delta_arr_client, delta_arr_server), "after deserialization of changed data, delta_arr_client and delta_arr_server are not identical"
    print("Modified array and deserialized modified array are identical")
