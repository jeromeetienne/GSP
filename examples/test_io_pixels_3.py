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
    positions_np = np.random.uniform(-1, +1, (n_points, 3)).astype(np.float32)

    # enable that when https://github.com/vispy/GSP/issues/14 is fixed
    # positions_vec3 = gsp.glm.to_vec3(positions_np)
    # pixels = visual.Pixels(positions=positions_vec3, colors=[0, 0, 0, 1])

    # workaround for now: create a raw buffer from numpy array - https://github.com/vispy/GSP/issues/14
    position_buffer = core.Buffer(count=positions_np.size, dtype=positions_np.dtype, data=positions_np.data)
    pixels = visual.Pixels(positions=position_buffer, colors=[0, 0, 0, 1])

    pixels.render(viewport)

    visuals = [pixels]
    return (canvas, viewport, visuals)

####################################################

if __name__ == "__main__":
    from examples.common.launcher import ExampleLauncher

    # Parse command line arguments
    gsp_core, gsp_visual = ExampleLauncher.parse_args(
        example_description="Example showing how to render a large number of pixels. NOTE: still buggy as it uses raw buffers"
    )

    # Run the main function
    canvas, viewport, visuals = main(core=gsp_core, visual=gsp_visual)

    # Show or save the result
    ExampleLauncher.show(canvas, viewport, visuals)
