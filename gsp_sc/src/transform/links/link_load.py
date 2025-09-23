from typing import Any
import typing
import numpy as np

from ..transform_link_base import TransformLinkBase
from ..transform_link_db import TransformLinkDB


class TransformLinkLoad(TransformLinkBase):

    def __init__(self, data_url: str):
        """
        Load data from a .npy file.
        """

        super().__init__()

        self.__data_url = data_url
        """The URL of the file to load"""
        self.__cached_data: np.ndarray | None = None

    def _run(self, np_array: np.ndarray) -> np.ndarray:
        # Load the data from the file if not already loaded
        if self.__cached_data is None:
            self.__cached_data = np.load(self.__data_url)

        # Return the cached data
        np_array = typing.cast(np.ndarray,self.__cached_data)
        return np_array 
    
    def _to_json(self) -> dict[str, Any]:
        return {
            "type": "TransformLoad",
            "data_url": self.__data_url
        }
    
    @staticmethod
    def _from_json(json_dict: dict[str, Any]) -> TransformLinkBase:
        data_url = json_dict["data_url"]
        return TransformLinkLoad(data_url)
    
# Register the TransformLoad class in the TransformLinkDB
TransformLinkDB.add_link("TransformLoad", TransformLinkLoad)