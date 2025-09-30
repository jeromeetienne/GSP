from typing import Any
import numpy as np
import json


class DeltaNdarray(np.ndarray):
    """
    A NumPy ndarray subclass that tracks the minimal bounding box of all modifications made to its elements.
    It works for n-dimensional arrays.
    The goal is to reduce the memory after serialisation and transfer over network, without
    increasing the local memory usage too much.

    ### Description
    This class extends `np.ndarray` to keep track of the smallest bounding box that contains
    all modifications made to the array. It overrides the `__setitem__` method to
    update the bounding box whenever elements are modified. The class provides methods to
    retrieve the bounding box and the modified region.

    ### Analysis
    Here we took the policy to have a single bounding box for all modifications.
    This may produce a larger bounding box than strictly necessary if modifications
    are scattered. To track per indice modifications, would reduce the serialised size
    further, but would increase the local memory usage.

    ### Possible other policies
    - Track per indice modifications (more memory usage, smaller serialised size)
    - Track single bounding box per axis (less memory usage, larger serialised size)
    - Track multiple bounding boxes (more memory usage, smaller serialised size, more complex code/maintenance)
    """

    def __new__(cls, input_array) -> "DeltaNdarray":
        obj = np.asarray(input_array).view(cls)
        obj._reset_delta()
        return obj

    def _reset_delta(self) -> None:
        self._delta_min = [None] * self.ndim
        self._delta_max = [None] * self.ndim

    def __setitem__(self, key, value) -> None:
        # Update delta bounds
        idx = self._normalize_key(key)
        self._update_delta_bounds(idx)
        super().__setitem__(key, value)

    def _normalize_key(self, key) -> list[tuple[int, int]]:
        # Convert key to a tuple of slices/indices for each axis
        if not isinstance(key, tuple):
            key = (key,)
        key = list(key) + [slice(None)] * (self.ndim - len(key))
        idx = []
        for i, k in enumerate(key):
            if isinstance(k, int):
                idx.append((k, k + 1))
            elif isinstance(k, slice):
                start, stop, step = k.indices(self.shape[i])
                idx.append((start, stop))
            else:
                raise TypeError(f"Unsupported index type: {type(k)}")
        return idx

    def _update_delta_bounds(self, idx) -> None:
        for axis, (start, stop) in enumerate(idx):
            if self._delta_min[axis] is None or start < self._delta_min[axis]:
                self._delta_min[axis] = start
            if self._delta_max[axis] is None or stop > self._delta_max[axis]:
                self._delta_max[axis] = stop

    def get_delta_slices(self) -> None | tuple[slice, ...]:
        if any(m is None for m in self._delta_min):
            return None  # No changes
        return tuple(slice(self._delta_min[i], self._delta_max[i]) for i in range(self.ndim))

    def get_delta(self) -> None | np.ndarray:
        slices = self.get_delta_slices()
        if slices is None:
            return None
        return self[slices]

    def clear_delta(self) -> None:
        self._reset_delta()

    def patch(self, slices: tuple[slice, ...], delta: np.ndarray) -> None:
        if slices is None:
            raise ValueError("Invalid slices")
        self[slices] = delta


    ###############################################################################
    #   JSON serialisation
    #

    def to_json(self) -> dict[str, Any]:
        delta_slices = self.get_delta_slices()

        # No modifications, serialize the whole array
        if delta_slices is None:
            json_dict = {
                "slices": None,
                "data": self.tolist(),
            }
            return json_dict

        # There are modifications, serialize only the delta region
        delta_data = self.get_delta()

        # Ensure the delta_data is valid
        assert delta_data is not None, "Delta data should not be None if delta slices exists"

        # Serialize the slices and the delta data
        json_dict = {
            "slices": DeltaNdarray.slice_to_json(delta_slices),
            "data": delta_data.tolist(),
        }
        return json_dict

    @staticmethod
    def from_json(json_dict: dict[str, Any], previous_arr: 'DeltaNdarray|None', in_place: bool = False) -> "DeltaNdarray":

        # No modifications, create a new DeltaNdarray with the full data
        if json_dict["slices"] is None:
            new_arr = DeltaNdarray(np.array(json_dict["data"]))
            return new_arr

        # from here, there are modifications to apply, so we need the previous array
        assert previous_arr is not None, "previous_arr must be provided if there are modifications to apply"

        # honor the in_place flag
        new_arr = previous_arr if in_place else DeltaNdarray(np.copy(previous_arr))

        # deserialize the slices
        slices = DeltaNdarray.slice_from_json(json_dict["slices"])

        # apply the patch
        new_arr.patch(slices, np.array(json_dict["data"]))

        return new_arr

    ###############################################################################
    #   Slice to/from JSON
    #
    @staticmethod
    def slice_to_json(slices: tuple[slice, ...]) -> dict[str, Any]:
        """
        Convert a tuple of slices to a JSON-serializable dictionary.
        """
        slice_dict = {"slices": [{"start": _slice.start, "stop": _slice.stop, "step": _slice.step} for _slice in slices]}
        return slice_dict

    @staticmethod
    def slice_from_json(slice_dict: dict[str, Any]) -> tuple[slice, ...]:
        """
        Convert a JSON-serializable dictionary back to a tuple of slices.
        """
        slices_tuple = tuple(slice(_slice["start"], _slice["stop"], _slice["step"]) for _slice in slice_dict["slices"])
        return slices_tuple


###############################################################################
#   Example usage
#
if __name__ == "__main__":
    delta_arr = DeltaNdarray(np.zeros((5, 5), dtype=int))
    # print(arr.get_delta())
    print("Initial array:\n", delta_arr)
    delta_arr[1, 2] = 10
    delta_arr[3:5, 1:4] = 5
    print("\nModified array:\n", delta_arr)
    print("\nDelta slice:", delta_arr.get_delta_slices())
    print("Delta region:\n", delta_arr.get_delta())

    # Serialize to JSON
    delta_arr_json_dict = delta_arr.to_json()
    delta_arr_json_str = json.dumps(delta_arr_json_dict, indent=4)
    print("\nSerialized to JSON:", delta_arr_json_str)

    # Deserialize from JSON
    delta_arr_loaded = DeltaNdarray.from_json(json.loads(delta_arr_json_str), delta_arr, in_place=False)
    print("\nDeserialized array:\n", delta_arr_loaded, "\nis delta_arr:", delta_arr_loaded is delta_arr)

    # Deserialize from JSON in-place
    delta_arr_loaded_inplace = DeltaNdarray.from_json(json.loads(delta_arr_json_str), delta_arr, in_place=True)
    print("\nDeserialized array (in-place):\n", delta_arr_loaded_inplace, "\nis delta_arr:", delta_arr_loaded_inplace is delta_arr)

    delta_arr.clear_delta()
    print("\nAfter clearing delta:", delta_arr.get_delta_slices())
