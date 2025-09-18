from typing import Any
import numpy as np

from ..transform_base import TransformBase


class TransformImmediate(TransformBase):

    def __init__(self, np_array: np.ndarray) -> None:
        """
        Load data from a .npy file.
        """
        super().__init__()

        self.__np_array = np_array

    def _run(self, np_array: np.ndarray) -> np.ndarray:
        # Do nothing and just return the data

        return self.__np_array

    # Serialization methods 

    def _to_json(self) -> dict[str, Any]:
        return {
            "type": "TransformImmediate",
            "np_array": self.__np_array.tolist()
        }
    
    @staticmethod
    def _from_json(json_dict: dict[str, Any]) -> TransformBase:
        np_array = np.array(json_dict["np_array"])
        return TransformImmediate(np_array)