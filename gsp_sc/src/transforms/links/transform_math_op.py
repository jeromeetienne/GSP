import numpy as np
from typing import Literal
from ..transform_base import TransformBase

class TransformMathOp(TransformBase):
    def __init__(self, operation: Literal["add", "sub", "mul", "div"], operand: float)  -> None:
        """
        Perform a math operation on the data.
        Supported operations: add, sub, mul, div
        """
        super().__init__()
        self.__operation = operation
        """The math operation to perform: add, sub, mul, div"""

        self.__operand = operand
        """The operand to use in the math operation"""

    def _run(self, np_array: np.ndarray) -> np.ndarray:
        if self.__operation == "add":
            result = np_array + self.__operand
        elif self.__operation == "sub":
            result = np_array - self.__operand
        elif self.__operation == "mul":
            result = np_array * self.__operand
        elif self.__operation == "div":
            result = np_array / self.__operand
        else:
            raise ValueError(f"Unsupported operation: {self.__operation}")

        return result