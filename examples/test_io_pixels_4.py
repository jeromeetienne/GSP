import numpy as np
from examples.common.launcher import parse_args

##############################################
# Parse command line arguments
#

core, visual, render = parse_args(
    example_description="Example showing how to render a large number of pixels. NOTE: still buggy as it uses raw buffers"
)

##############################################
# Create a GSP scene
#

# Create a canvas and a viewport
canvas = core.Canvas(512, 512, 100.0)
viewport = core.Viewport(canvas, 0, 0, 512, 512, [1, 1, 1, 1])

##############################################
# Create a large number of random pixels
#

n_points = 200_000
positions_np = np.random.uniform(-1, +1, (n_points, 3)).astype(np.float32)

# enable that when https://github.com/vispy/GSP/issues/14 is fixed
# positions_vec3 = gsp.glm.to_vec3(positions_np)
# pixels = visual.Pixels(positions=positions_vec3, colors=[0, 0, 0, 1])

# workaround for now: create a raw buffer from numpy array - https://github.com/vispy/GSP/issues/14
position_buffer = core.Buffer(count=positions_np.size, dtype=positions_np.dtype, data=positions_np.data)
pixels = visual.Pixels(positions=position_buffer, colors=[0, 0, 0, 1])
pixels.render(viewport)

#############################################
# Show or save the result
#

render(canvas, [viewport], [pixels])
