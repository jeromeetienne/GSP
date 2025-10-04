from dataclasses import dataclass
from re import split
from tracemalloc import start
from typing import Any
import numpy as np
import json
import typing
from gsp_sc.tmp.delta_ndarray.delta_ndarray import DeltaNdarray
from dataclasses import dataclass

# TODO to rename DiffableNdarray ?
class DeltaNdarraySerialisation:
    ###############################################################################
    #   JSON serialisation
    #

    @staticmethod
    def to_json(delta_ndarray: DeltaNdarray, diff_allowed: bool = False) -> dict[str, Any]:
        """
        Serialize the DeltaNdarray to a JSON-serializable dictionary.
        """

        # No modifications, serialize the whole array
        if diff_allowed == False or delta_ndarray.is_modified() is False:
            json_dict = {
                "slices": None,
                "data": delta_ndarray.tolist(),
            }
            return json_dict

        # There are modifications, serialize only the delta region
        delta_slices = DeltaNdarray.get_delta_slices(delta_ndarray)
        delta_region = DeltaNdarray.get_delta_data(delta_ndarray)

        # Ensure the delta_region is valid
        assert delta_region is not None, "Delta region should not be None if delta slices exists"

        # Serialize the slices and the delta region
        json_dict = {
            "slices": DeltaNdarraySerialisation._slice_to_json(delta_slices),
            "data": delta_region.tolist(),
        }
        return json_dict

    @staticmethod
    def from_json(json_dict: dict[str, Any], previous_arr: "DeltaNdarray|None") -> "DeltaNdarray":
        """
        Deserialize a JSON-serializable dictionary back to a DeltaNdarray.
        """

        # No modifications, create a new DeltaNdarray with the full data
        if json_dict["slices"] is None:
            new_arr = DeltaNdarray(np.array(json_dict["data"]))
            return new_arr

        # from here, there are modifications to apply, so we need the previous array
        assert previous_arr is not None, "previous_arr must be provided if there are modifications to apply"

        # honor the in_place flag
        new_arr = previous_arr.copy()

        # deserialize the slices
        slices = DeltaNdarraySerialisation._slice_from_json(json_dict["slices"])

        # apply the patch
        new_arr.apply_patch(slices, np.array(json_dict["data"]))

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
            # bla
            "slices": [
                {
                    # bli
                    "start": _slice.start,
                    "stop": _slice.stop,
                    "step": _slice.step,
                }
                for _slice in slices
            ]
        }
        return slice_dict

    @staticmethod
    def _slice_from_json(slice_dict: dict[str, Any]) -> tuple[slice, ...]:
        """
        Convert a JSON-serializable dictionary back to a tuple of slices.
        """
        slices_arr = [slice(_slice["start"], _slice["stop"], _slice["step"]) for _slice in slice_dict["slices"]]
        slices_tuple = tuple(slices_arr)
        return slices_tuple


###############################################################################
#   Example usage
#
if __name__ == "__main__":
    ###############################################################################
    #   Example usage without modifications - client side
    #
    delta_arr_client = DeltaNdarray(np.arange(25).reshape(5, 5))
    print("*" * 80)
    print("Initial array:\n", delta_arr_client)
    print("Is modified:", delta_arr_client.is_modified())

    delta_arr_client_dict = DeltaNdarraySerialisation.to_json(delta_arr_client)

    ###############################################################################
    #   Example usage without modifications - server side
    #

    delta_arr_server = None
    delta_arr_server = DeltaNdarraySerialisation.from_json(delta_arr_client_dict, delta_arr_server)

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
    print("Delta slice:", delta_arr_client.get_delta_slices())
    print("Delta region:\n", delta_arr_client.get_delta_data())
    print("Modified array:\n", delta_arr_client)

    # Serialize to JSON
    delta_arr_json_dict = DeltaNdarraySerialisation.to_json(delta_arr_client)
    # Clear delta in client array after serialisation
    delta_arr_client.clear_delta()
    print("\nAfter serialisation and clearing delta: is_modified=", delta_arr_client.is_modified())

    ###############################################################################
    #   Example usage with modifications - server side
    #
    # Deserialize from JSON
    delta_arr_server = DeltaNdarraySerialisation.from_json(delta_arr_json_dict, delta_arr_server)
    print("\nDeserialized array:\n", delta_arr_server)
    print("Is modified:", delta_arr_server.is_modified())
    # check delta_arr_client and delta_arr_server are identical
    assert np.array_equal(delta_arr_client, delta_arr_server), "after deserialization of changed data, delta_arr_client and delta_arr_server are not identical"
    print("Modified array and deserialized modified array are identical")
