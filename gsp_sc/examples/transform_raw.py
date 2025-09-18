import gsp_sc.src as gsp_sc
import numpy as np
import os
from gsp_sc.src.transform import TransformLinkLoad, TransformLinkMathOp, TransformLinkImmediate


__dirname__ = os.path.dirname(os.path.abspath(__file__))
url_npy = f"{__dirname__}/data/sample.npy"

myTransform1 = (
    TransformLinkLoad(data_url=url_npy)
    .chain(TransformLinkMathOp("add", 5))
    .chain(TransformLinkMathOp("mul", 2))
)

np_array1 = myTransform1.run()
print(f"Loaded array1: {np_array1}")

###############################################################################

myTransform2 = (
    TransformLinkImmediate(np.array([10, 20, 30]))
    .chain(TransformLinkMathOp("add", 5))
    .chain(TransformLinkMathOp("mul", 2))
)

np_array2 = myTransform2.run()
print(f"Loaded array2: {np_array2}")
