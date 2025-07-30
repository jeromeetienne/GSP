import numpy as np

# declare an numpy array shape (5,2) with value from 0 to 9
array_1 = np.ndarray(shape=[5,2], buffer=np.array([0,1,2,3,4,5,6,7,8,9]), dtype=np.int64)

print(f"Array_1[0]: {array_1[0]}")
print(f"Array_1[len(array_1)-5]: {array_1[len(array_1)-5]}")

