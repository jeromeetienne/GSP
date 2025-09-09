class Cmdline_Args:
    @staticmethod
    def parse_args()->tuple:
        import argparse

        args:dict = {
            "command": "generate_command_file",
            "command_file_cycle": True
        }
        args['command'] = "generate_command_file"
        args['command_file_cycle'] = True
        # args['command'] = "matplotlib_show"

        # discover the example basename
        example_basename = os.path.basename(__file__).replace(".py", "")
        print(f"Running {example_basename} with command '{args['command']}'")

        if args["command"] not in ["generate_command_file", "matplotlib_show"]:
            raise ValueError(f"Unknown command: {args['command']}")

        if args["command"] == "generate_command_file":
            gsp_core = gsp.core
            gsp_visual = gsp.visual
        elif args["command"] == "matplotlib_show":
            gsp_core = gsp.matplotlib.core
            gsp_visual = gsp.matplotlib.visual
        else:
            raise ValueError(f"Unknown command: {args['command']}")

        return gsp_core, gsp_visual, args, example_basename

    @staticmethod
    def postprocess( args, example_basename):
        import matplotlib.pyplot as plt
        
        if args["command"] == "generate_command_file":
            commands_filename = f"{os.path.dirname(os.path.abspath(__file__))}/output/{example_basename}.commands.json"
            gsp.save(commands_filename)

            # Re-load commands and re-execute them
            if args["command_file_cycle"] == True:

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
        elif args["command"] == "matplotlib_show":
            import matplotlib.pyplot as plt

            # save a screenshot of the rendered canvas
            image_filename = f"{os.path.dirname(os.path.abspath(__file__))}/output/{example_basename}.png"
            plt.savefig(image_filename)

            plt.show(block=True)
        else:
            print(f"Unknown command: {args.command}")

