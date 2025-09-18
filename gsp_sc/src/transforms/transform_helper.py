from typing import Literal

from .links import (
    TransformLoad,
    TransformMathOp,
    TransformImmediate,
    TransformAssertShape,
)
from .transform_base import TransformBase
import numpy as np

class TransformHelper:
    def __init__(self, np_array: np.ndarray | None = None) -> None:
        """
        Initialize the TransformHelper with an optional initial numpy array.
        """
        self._transform_chain: TransformBase | None = None

        if np_array is not None:
            self.immediate(np_array)

    def get_transform_chain(self) -> TransformBase:
        """
        Get the current transformation chain.
        """
        if self._transform_chain is None:
            raise ValueError("No transformation chain defined.")
        return self._transform_chain
    
    def has_transform_chain(self) -> bool:
        """
        Check if a transformation chain is defined.
        """
        return self._transform_chain is not None

    def run(self) -> np.ndarray:
        """
        Run the transformation chain and return the resulting numpy array.
        """

        if self._transform_chain is None:
            # If no transforms, return empty array
            np_array = np.array([])
        else:
            # Run the chain of transforms
            np_array = self._transform_chain.run()

        # return the re
        return np_array
    
    def __chain(self, new_transform: TransformBase) -> "TransformHelper":
        """
        Chain a new transformation to the existing transformation chain.
        """

        if self._transform_chain is None:
            self._transform_chain = new_transform
        else:
            self._transform_chain = self._transform_chain.chain(new_transform)

        return self



	#####################################################################################
    # Transformation methods
    # FIXME those hardcoded strings are error-prone and should be avoided - have that to be dynamic - similar in transform_helper.py
    #

    def assert_shape(self, expected_shape: tuple[int, ...]) -> "TransformHelper":
        """
        Ensure the input array has the specified shape.
        """
        new_transform = TransformAssertShape(expected_shape)
        
        return self.__chain(new_transform)

    def immediate(self, np_array: np.ndarray) -> "TransformHelper":
        """
        Use the provided numpy array as the initial data.
        """
        new_transform = TransformImmediate(np_array)

        return self.__chain(new_transform)

    def load(self, data_url: str) -> "TransformHelper":
        """
        Load a numpy array from the specified .npy file URL.
        """
        new_transform = TransformLoad(data_url)
        
        return self.__chain(new_transform)

    def math_op(
        self, operation: Literal["add", "sub", "mul", "div"], operand: float
    ) -> "TransformHelper":
        """
        Perform a math operation on the data.
        """
        new_transform = TransformMathOp(operation, operand)

        return self.__chain(new_transform)

