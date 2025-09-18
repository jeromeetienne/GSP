import numpy as np

# TODO
# - TransformLoad load a .npy file
# - TransformMathOp do math operation 
#   - add, sub, mul, div

class TransformBase:
    """
    Base class for data transformations.
    Each transformation can be chained to another transformation.
    """
    def __init__(self):
        self.next_transform: TransformBase | None = None
        self.previous_transform: TransformBase | None = None


    def chain(self, other_transform: 'TransformBase') -> 'TransformBase':
        other_transform.previous_transform = self
        self.next_transform = other_transform

        return self.next_transform
    
    def _run(self, np_array: np.ndarray) -> np.ndarray:
        raise NotImplementedError("_run method must be implemented by subclasses")

    def run(self) -> np.ndarray:
        # Find the first transform in the chain
        first_transform = self
        while first_transform.previous_transform is not None:
            first_transform = first_transform.previous_transform

        # Run the chain of transforms
        np_array = np.empty((0,))  # Start with an empty array
        current_transform = first_transform
        while current_transform is not None:
            # Run this transform
            np_array = current_transform._run(np_array)
            # Move to the next transform
            current_transform = current_transform.next_transform

        return np_array
        
