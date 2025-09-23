"""
Run example scripts in this directory sequentially.
It helps testing that all examples run without errors.
"""

import argparse
import subprocess
import sys
import os

__dirname__ = os.path.dirname(os.path.abspath(__file__))

def launch_example(cmdline_args: list[str], debug: bool = False) -> bool:
    """
    Launches the example script with the given command line arguments.

    Arguments:
        cmdline_args: List of command line arguments to pass to the script.

    Returns:
        True if the script ran successfully, False otherwise.
    """

    if debug:
        print(f"Launching example with args: {cmdline_args}")

    try:
        # Add a environment variable to disable interactive mode in the example
        env = dict(**os.environ, GSP_SC_INTERACTIVE="False")

        result = subprocess.run(
            cmdline_args,
            check=True,  # Raises CalledProcessError if script fails
            capture_output=True,
            text=True,  # Capture output as string instead of bytes
            env=env,
        )
        run_success = True if result.returncode == 0 else False

    except subprocess.CalledProcessError as e:
        run_success = False

    return run_success


###############################################################################
# Main script logic
#

def split_argv():
    if '--' not in sys.argv:
        local_args = sys.argv[1:]
        launcher_args = []
    else:
        separator_index = sys.argv.index('--')
        local_args = sys.argv[1:separator_index]
        launcher_args = sys.argv[separator_index + 1:]
    return local_args, launcher_args

def main()->None:
    # Split local args and launcher.py args
    local_args, launcher_args = split_argv()

    # parse command line arguments
    parser = argparse.ArgumentParser(description="Run all example scripts in this directory.")
    parser.add_argument("--debug", action="store_true", help="Enable debug mode with more verbose output.")
    args = parser.parse_args(local_args)

    # Set debug mode
    if args.debug:
        print("Debug mode is enabled.")

    examples_folder = f"{__dirname__}/../examples"
    script_paths = [
        f"{examples_folder}/canvas-base.py",
        f"{examples_folder}/canvas-save.py",
        f"{examples_folder}/io_inheritance.py",
        f"{examples_folder}/io_saveload.py",
        f"{examples_folder}/lidar-point-cloud.py",
        f"{examples_folder}/markers-2d.py",
        f"{examples_folder}/markers-3d.py",
        f"{examples_folder}/paths-2d.py",
        f"{examples_folder}/paths-3d.py",
        f"{examples_folder}/paths-regular-2d.py",
        f"{examples_folder}/pixels-2d.py",
        f"{examples_folder}/pixels-3d.py",
        f"{examples_folder}/pixels-colormap.py",
        f"{examples_folder}/pixels-colors.py",
        f"{examples_folder}/pixels-interactive.py",
        f"{examples_folder}/points-2d.py",
        f"{examples_folder}/points-3d.py",
        f"{examples_folder}/points-colormap.py",
        f"{examples_folder}/polygons-2d.py",
        f"{examples_folder}/segments-2d.py",
        f"{examples_folder}/segments-fixed-size.py",
        f"{examples_folder}/viewport-multiple.py",
        f"{examples_folder}/viewport-with-margins.py",
    ]

    for script_path in script_paths:
        # display the basename of the script without new line, and flush the output
        basename_script = os.path.basename(script_path)
        print(f"Running {basename_script} ... ", end="", flush=True)

        # launch the example script
        run_success = launch_example([sys.executable, script_path, *launcher_args])

        # display X in red if failed, or a check in green if successful
        if run_success:
            print("\033[92mOK\033[0m")  # Green "OK"
        else:
            print("\033[91mFailed\033[0m")  # Red "Failed"

        # if not run_success:
        #     sys.exit(1)


if __name__ == "__main__":
    main()
