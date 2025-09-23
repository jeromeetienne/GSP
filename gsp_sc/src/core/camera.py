from typing import Literal
import numpy as np

import mpl3d.camera

from .random import Random

class Camera:
    __slots__ = ["uuid", "camera_type", "__mpl3d_camera"]
    
    def __init__(self, camera_type: Literal["ortho", "perspective"]):
        self.uuid = Random.random_uuid()
        """The unique identifier of the camera."""
        
        self.camera_type = camera_type
        """The type of camera: "ortho" or "perspective" """

        self.__mpl3d_camera = mpl3d.camera.Camera(mode=camera_type)
        """The internal mpl3d camera """

    # A getter for the internal mpl3d camera.transform
    @property
    def transform(self) -> np.ndarray:
        return self.__mpl3d_camera.transform
    
    @property
    def mpl3d_camera(self) -> mpl3d.camera.Camera:
        return self.__mpl3d_camera