import numpy as np

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

    def __new__(cls, input_array):
        obj = np.asarray(input_array).view(cls)
        obj._reset_delta()
        return obj

    def _reset_delta(self):
        self._delta_min = [None] * self.ndim
        self._delta_max = [None] * self.ndim

    def __setitem__(self, key, value):
        # Update delta bounds
        idx = self._normalize_key(key)
        self._update_delta_bounds(idx)
        super().__setitem__(key, value)

    def _normalize_key(self, key):
        # Convert key to a tuple of slices/indices for each axis
        if not isinstance(key, tuple):
            key = (key,)
        key = list(key) + [slice(None)] * (self.ndim - len(key))
        idx = []
        for i, k in enumerate(key):
            if isinstance(k, int):
                idx.append((k, k+1))
            elif isinstance(k, slice):
                start, stop, step = k.indices(self.shape[i])
                idx.append((start, stop))
            else:
                raise TypeError(f"Unsupported index type: {type(k)}")
        return idx

    def _update_delta_bounds(self, idx):
        for axis, (start, stop) in enumerate(idx):
            if self._delta_min[axis] is None or start < self._delta_min[axis]:
                self._delta_min[axis] = start
            if self._delta_max[axis] is None or stop > self._delta_max[axis]:
                self._delta_max[axis] = stop

    def get_delta_slice(self):
        if any(m is None for m in self._delta_min):
            return None  # No changes
        return tuple(slice(self._delta_min[i], self._delta_max[i]) for i in range(self.ndim))

    def get_delta(self):
        s = self.get_delta_slice()
        if s is None:
            return None
        return self[s]

    def clear_delta(self):
        self._reset_delta()


if __name__ == "__main__":
    # Example usage
    arr = DeltaNdarray(np.zeros((5, 5), dtype=int))
    print("Initial array:\n", arr)
    arr[1, 2] = 10
    arr[3:5, 1:4] = 5
    print("\nModified array:\n", arr)
    print("\nDelta slice:", arr.get_delta_slice())
    print("Delta region:\n", arr.get_delta())
    arr.clear_delta()
    print("\nAfter clearing delta:", arr.get_delta_slice())
