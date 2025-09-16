from gsp import glm
from gsp.matplotlib import ndarray_to_Buffer
import numpy as np

vec3_array1 = glm.vec3(1)

import gsp

# Save a command file
import os
__dirname__ = os.path.dirname(os.path.abspath(__file__))
commands_filename = f"{__dirname__}/output/{os.path.basename(__file__).replace('.py', '')}.command.json"
gsp.save(filename=commands_filename)
