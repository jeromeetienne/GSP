import numpy as np
import typing

class DiffableNdarray(np.ndarray):

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

    def __new__(cls, input_array) -> "DiffableNdarray":
        obj = np.asarray(input_array).view(cls)
        obj._delta_min = typing.cast(list[int | None], [None] * obj.ndim)
        obj._delta_max = typing.cast(list[int | None], [None] * obj.ndim)
        return obj
    
    def __array_finalize__(self, obj):
        # This method is called automatically after the object is created,
        # both when new instances are created and when slicing happens.
        if obj is None:
            return
        # Copy the attribute from the original object (if it exists)
        self._delta_min = obj._delta_min if hasattr(obj, '_delta_min') else [None] * self.ndim
        self._delta_max = obj._delta_max if hasattr(obj, '_delta_max') else [None] * self.ndim

    def _reset_diff(self) -> None:
        self._delta_min: list[int | None] = [None] * self.ndim
        self._delta_max: list[int | None] = [None] * self.ndim

    def __setitem__(self, key, value) -> None:
        # Update delta bounds
        idx = self._normalize_key(key)
        self._update_delta_minmax(idx)
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

    def _update_diff_minmax(self, idx) -> None:
        for axis, (start, stop) in enumerate(idx):
            if self._delta_min[axis] is None or start < self._delta_min[axis]:
                self._delta_min[axis] = start
            if self._delta_max[axis] is None or stop > self._delta_max[axis]:
                self._delta_max[axis] = stop

    def _get_diff_slices(self) -> None | tuple[slice, ...]:
        if any(m is None for m in self._delta_min):
            return None  # No changes
        return tuple(slice(self._delta_min[i], self._delta_max[i]) for i in range(self.ndim))

    ###############################################################################
    #   Public API
    #


    def copy(self, order="C") -> "DiffableNdarray":
        """
        Create a copy of the DeltaNdarray, including its modification tracking state.
        """
        new_copy = super().copy(order=order).view(DiffableNdarray)
        new_copy._delta_min = self._delta_min.copy()
        new_copy._delta_max = self._delta_max.copy()
        return new_copy

    def is_modified(self) -> bool:
        slices = self._get_delta_slices()
        return slices is not None

    def get_diff_slices(self) -> tuple[slice, ...]:
        """
        Return the slices that define the bounding box of all modifications.
        Raises a assertion error if there are no modifications (use is_modified() to check).
        """
        diff_slices = self._get_diff_slices()
        assert diff_slices is not None, "No modifications to get diff slices from (use is_modified() to check)"

        return diff_slices

    def get_diff_data(self) -> np.ndarray:
        """
        Return the modified region of the array.
        Raises an assertion error if there are no modifications (use is_modified() to check).
        """
        diff_slices = self._get_diff_slices()
        assert diff_slices is not None, "No modifications to get diff data from (use is_modified() to check)"

        diff_data: np.ndarray = self[diff_slices]

        return diff_data
    
    def clear_diff(self) -> None:
        """ 
        Clear the modification tracking.
        After calling this method, the array is considered unmodified until further changes are made.
        """
        self._reset_diff()

    def apply_patch(self, diff_slices: tuple[slice, ...], diff_region: np.ndarray) -> None:
        """
        Apply a patch to the array at the specified slices with the provided diff data.
        """
        self[diff_slices] = diff_region


###############################################################################
#   Example usage
#
if __name__ == "__main__":
    ###############################################################################
    #   Example usage without modifications
    #
    diffable_arr = DiffableNdarray(np.arange(25).reshape(5,5))

    print('*' * 80)
    print("Initial array:\n", diffable_arr)
    print("Is modified:", diffable_arr.is_modified())
    assert diffable_arr.is_modified() == False, "Array should be marked as modified"
    
    ###############################################################################
    #   Example usage with modifications
    #

    diffable_arr[1, 2] = -50
    diffable_arr[3:5, 1:4] = -60
    assert diffable_arr.is_modified() == True, "Array should be marked as modified"

    print("Is modified:", diffable_arr.is_modified())
    print("Delta slice:", diffable_arr.get_diff_slices())
    print("Delta region:\n", diffable_arr.get_diff_data())
    print("Modified array:\n", diffable_arr)
