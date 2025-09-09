import os
import numpy as np
import gsp


def main(core: gsp.core, visual: gsp.visual):
    canvas = core.Canvas(512, 512, 100.0)
    viewport = core.Viewport(canvas, 0, 0, 512, 512, [1, 1, 1, 1])

    n_points = 200_000
    positions_np = np.random.uniform(-1, +1, (n_points, 3)).astype(np.float32)
    # positions_np = np.ones((n_points,3), dtype=np.float32)
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
    import argparse

    args: argparse.Namespace = argparse.Namespace()
    args.command = "generate_command_file"
    args.command_file_cycle = True
    args.command = "matplotlib_show"

    # discover the example basename
    example_basename = os.path.basename(__file__).replace(".py", "")
    print(f"Running {example_basename} with command '{args.command}'")

    if args.command not in ["generate_command_file", "matplotlib_show"]:
        raise ValueError(f"Unknown command: {args.command}")

    if args.command == "generate_command_file":
        gsp_core = gsp.core
        gsp_visual = gsp.visual
    elif args.command == "matplotlib_show":
        gsp_core = gsp.matplotlib.core
        gsp_visual = gsp.matplotlib.visual
    else:
        raise ValueError(f"Unknown command: {args.command}")

    ###################################################

    main(core=gsp_core, visual=gsp_visual)

    ###################################################

    if args.command == "generate_command_file":
        commands_filename = f"{os.path.dirname(os.path.abspath(__file__))}/output/{example_basename}.commands.json"
        gsp.save(commands_filename)

        # Re-load commands and re-execute them
        if args.command_file_cycle == True:

            # reset objects
            gsp.Object.objects = {}

            # load commands from file
            command_queue = gsp.io.json.load(commands_filename)

            import logging

            gsp.log.setLevel(logging.INFO)
            for command in command_queue:
                gsp.log.info("%s" % command)

            # KEY: REQUIRED FOR THE GLOBALS - Super dirty!!!
            gsp.use("matplotlib")

            # TODO send matplotlib as namespace in command_queue.run
            command_queue.run(globals(), locals())
            print(f"object: {gsp.Object.objects[1]}")

            plt.show(block=True)
    elif args.command == "matplotlib_show":
        import matplotlib.pyplot as plt

        # save a screenshot of the rendered canvas
        image_filename = f"{os.path.dirname(os.path.abspath(__file__))}/output/{example_basename}.png"
        plt.savefig(image_filename)

        plt.show(block=True)
    else:
        print(f"Unknown command: {args.command}")
