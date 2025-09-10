import os
import matplotlib.image as mpl_img
import gsp

def main(
    core: gsp.core, visual: gsp.visual
) -> tuple[
    gsp.core.viewport.Canvas, gsp.core.viewport.Viewport, list[gsp.visual.visual.Visual]
]:

    canvas = core.Canvas(256, 256, 100.0)
    viewport = core.Viewport(canvas, 0, 0, 256, 256, [1, 1, 1, 1])

    ######

    cube_path_positions = gsp.glm.vec3(8)
    cube_path_positions[...] = [
        (-1.0, -1.0, +1.0),
        (+1.0, -1.0, +1.0),
        (-1.0, +1.0, +1.0),
        (+1.0, +1.0, +1.0),
        (-1.0, -1.0, -1.0),
        (+1.0, -1.0, -1.0),
        (-1.0, +1.0, -1.0),
        (+1.0, +1.0, -1.0),
    ]
    cube_path_face_indices = [
        [0, 1],
        [1, 3],
        [3, 2],
        [2, 0],
        [4, 5],
        [5, 7],
        [7, 6],
        [6, 4],
        [0, 4],
        [1, 5],
        [2, 6],
        [3, 7],
    ]

    colormap = gsp.transform.Colormap("gray", vmin=0.0, vmax=0.75)
    depth = gsp.transform.Out("screen[paths].z")
    paths_visual = visual.Paths(
        cube_path_positions,
        cube_path_face_indices,
        line_colors=colormap(depth),
        line_widths=5.0 * (1 - 1.25 * depth),
        line_styles=gsp.core.LineStyle.solid,
        line_joins=gsp.core.LineJoin.round,
        line_caps=gsp.core.LineCap.round,
    )
    paths_visual.render(viewport)

    #####################################################################
    # Add an image visual
    #

    # Read the image_data numpy array from a file
    image_path = f"{os.path.dirname(os.path.abspath(__file__))}/images/UV_Grid_Sm.jpg"
    image_data_np = mpl_img.imread(image_path)

    image_visual = visual.Image(
        positions=[[-1, 1, -1]],
        image_data=image_data_np,
        image_extent=(-1, 1, -1, 1),
    )
    image_visual.render(viewport)

    visuals = [image_visual, paths_visual]
    return (canvas, viewport, visuals)

if __name__ == "__main__":
    from examples.libs.example_args_parse import ExampleArgsParse

    # Parse command line arguments
    gsp_core, gsp_visual = ExampleArgsParse.parse(
        example_description="Example showing how to render an image in 3d."
    )

    # Run the main function
    canvas, viewport, visuals = main(core=gsp_core, visual=gsp_visual)

    # Post-process command line arguments
    ExampleArgsParse.show(canvas, viewport, visuals)
