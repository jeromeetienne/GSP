import gsp_sc.src as gsp_sc
import numpy as np
import os
from gsp_sc.src.transforms import TransformHelper as Transform


__dirname__ = os.path.dirname(os.path.abspath(__file__))
url_npy = f"{__dirname__}/data/sample.npy"

np_array2 = Transform().load(url_npy).math_op("add", 3).run()
print(f'np_array2:{np_array2}')

np_array3 = Transform(np.array([1, 2, 3])).assert_shape((3,)).math_op("mul", 10).run()
print(f'np_array3:{np_array3}')

np_array4 = Transform().run()
print(f'np_array4:{np_array4}')
