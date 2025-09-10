import os
import numpy as np
import gsp


def main(core: gsp.core, visual: gsp.visual):
    canvas = core.Canvas(512, 512, 100.0)
    viewport = core.Viewport(canvas, 0, 0, 512, 512, [1, 1, 1, 1])

    n_points = 200_000
    positions_np = np.random.uniform(-1, +1, (n_points, 3)).astype(np.float32)
    positions_vec3 = positions_np

    buffer_count = positions_vec3.size
    buffer_dtype = positions_vec3.dtype
    buffer_data = positions_vec3.data

    position_buffer = core.Buffer(buffer_count, buffer_dtype, buffer_data)

    # position_vec3_bis = glm.to_vec3(position_buffer)
    pixels = visual.Pixels(position_buffer, colors=[0, 0, 0, 1])
    pixels.render(viewport)

####################################################


if __name__ == "__main__":
    from libs.cmdline_args import Cmdline_Args

    # Parse command line arguments
    gsp_core, gsp_visual = Cmdline_Args.preprocess()

    # Run the main function
    main(core=gsp_core, visual=gsp_visual)

    # Post-process command line arguments
    Cmdline_Args.postprocess()

