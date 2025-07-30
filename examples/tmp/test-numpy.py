print(*range(0, 10))

import numpy as np

# v = np.random.rand(10)

# Declare a variable u of shape (5,2) with value from 0 to 9
u = np.ndarray(shape=[5,2], buffer=np.array([0,1,2,3,4,5,6,7,8,9]), dtype=np.int64)

v = np.ndarray(shape=[10], buffer=np.array([0,1,2,3,4,5,6,7,8,9]), dtype=np.int64)
# v = np.array([0,1,2,3,4,5,6,7,8,9], dtype=np.int64)



print(v)
print(f'type of v is {type(v)}')
# display the main informations about the array v
print(f'v.shape: {v.shape}')
print(f'v.dtype: {v.dtype}')
print(f'v.size: {v.size}')
print(f'v.itemsize: {v.itemsize}')
print(f'v.nbytes: {v.nbytes}')
print(f'v.strides: {v.strides}')
print(f'v.flags: {v.flags}')
print(f'v.base: {v.base}')

v2 = v.view(dtype=np.float64)
print(f'v2.base: {v2.base}')  # should be None, as v2 is a view of v
print(f'v2.shape: {v2.shape}')
print(f'v2.dtype: {v2.dtype}')
print(f'v2.base: {v2.base}')
print(f'v2 base is v: {v2.base is v}')  # should be True, as v2 is a view of v

exit()