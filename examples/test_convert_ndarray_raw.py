from gsp import glm
from gsp.matplotlib import ndarray_to_Buffer
import numpy as np

vec3_array1 = glm.vec3(10, dtype=np.float32)
# vec3_array1 = np.ndarray(10)

vec3_buffer = ndarray_to_Buffer(vec3_array1)
print(f"vec3_array1: {vec3_array1}")

# vec3_array2 = glm.to_vec3(vec3_buffer)
# print(f"vec3_array2: {vec3_array2}")