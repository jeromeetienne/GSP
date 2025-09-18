from typing import Any
import numpy as np

from ..transform_base import TransformBase

class TransformLoad(TransformBase):

    def __init__(self, data_url: str):
        """
        Load data from a .npy file.
        """

        super().__init__()

        self.__data_url = data_url
        """The URL of the file to load"""

    def _run(self, np_array: np.ndarray) -> np.ndarray:
        np_array = np.load(self.__data_url)
        
        return np_array 
    
    def _to_json(self) -> dict[str, Any]:
        return {
            "type": "TransformLoad",
            "data_url": self.__data_url
        }
    
    @staticmethod
    def _from_json(json_dict: dict[str, Any]) -> TransformBase:
        data_url = json_dict["data_url"]
        return TransformLoad(data_url)