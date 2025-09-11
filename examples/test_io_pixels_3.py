import numpy as np
import gsp

def main(
    core: gsp.core, visual: gsp.visual
) -> tuple[
    gsp.core.viewport.Canvas, gsp.core.viewport.Viewport, list[gsp.visual.visual.Visual]
]:
    canvas = core.Canvas(512, 512, 100.0)
    viewport = core.Viewport(canvas, 0, 0, 512, 512, [1, 1, 1, 1])

    n_points = 200_000
    positions = gsp.glm.to_vec3(np.random.uniform(-1, +1, (n_points,2)), dtype=np.float32)
    # positions_np2 = np.ndarray(positions_np)

    positions_np = np.random.uniform(-1, +1, (n_points, 3)).astype(np.float32)
    buffer_count = positions_np.size
    buffer_dtype = positions_np.dtype
    buffer_data = positions_np.data
    position_buffer = core.Buffer(buffer_count, buffer_dtype, buffer_data)

    # position_vec3_bis = glm.to_vec3(position_buffer)
    pixels = visual.Pixels(positions=position_buffer, colors=[0, 0, 0, 1])
    pixels.render(viewport)

    visuals = [pixels]
    return (canvas, viewport, visuals)

####################################################

if __name__ == "__main__":
    from examples.common.example_args_parse import ExampleArgsParse

    # Parse command line arguments
    gsp_core, gsp_visual = ExampleArgsParse.parse(
        example_description="Example showing how to render a large number of pixels."
    )

    # Run the main function
    canvas, viewport, visuals = main(core=gsp_core, visual=gsp_visual)

    # Show or save the result
    ExampleArgsParse.show(canvas, viewport, visuals)
