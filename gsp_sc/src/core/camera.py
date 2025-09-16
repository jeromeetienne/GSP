from typing import Literal
import numpy as np
import uuid

import mpl3d.camera

class Camera:
    def __init__(self, camera_type: Literal["ortho", "perspective"]):
        self.uuid = str(uuid.uuid4())
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