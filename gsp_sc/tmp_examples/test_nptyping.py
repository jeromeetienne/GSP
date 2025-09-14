from nptyping import NDArray, Shape, Float64, Float32
import nptyping
from beartype import beartype
import numpy as np

@beartype
def bar(arr: NDArray[Shape["*, 3"], nptyping.Float]):
    # sanity check - np.ndarray type checking at runtime
    assert arr.shape[1:] == (3,)

    print(arr)

array1 = np.array([[1.0, 2.0, 3.0],
                   [4.0, 5.0, 6.0],
                   [4.0, 5.0, 6.0],
                   [7.0, 8.0, 9.0]], dtype=np.float64)
bar(array1)  # This should work