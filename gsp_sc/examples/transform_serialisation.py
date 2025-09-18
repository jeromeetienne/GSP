import gsp_sc.src as gsp_sc
import numpy as np
import os
import json
from gsp_sc.src.transform import TransformChain
from gsp_sc.src.transform import TransformSerialisation

__dirname__ = os.path.dirname(os.path.abspath(__file__))

# Create a Transform chain
transform_chain = TransformChain(np.array([1, 2, 3])).assert_shape((3,)).math_op("mul", 10).get_transform_chain()
print(f"transform_chain: {transform_chain}")

# Convert to JSON
json_array = TransformSerialisation.to_json(transform_chain)

# Pretty print the JSON
print(f"json_array: {json.dumps(json_array, indent=8)}")

# Recreate the Transform chain from JSON
transform_deserialized = TransformSerialisation.from_json(json_array)

# Run the deserialized transform chain
np_array = transform_deserialized.run()

# Display the result
print(f"np_array_deserialized: {np_array}")

assert np.array_equal(np_array, np.array([10, 20, 30])), "Deserialized transform did not produce the expected result"
