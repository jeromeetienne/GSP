from posixpath import basename
import subprocess
import sys
import os


def launch_example(cmdline_args: list[str]) -> bool:
    """
    Launches the example script with the given command line arguments.

    Arguments:
        cmdline_args: List of command line arguments to pass to the script.

    Returns:
        True if the script ran successfully, False otherwise.
    """
    try:
        # Add a environment variable to disable interactive mode in the example
        env = dict(**os.environ, GSP_SC_INTERACTIVE="False")

        result = subprocess.run(
            cmdline_args,
            check=True,  # Raises CalledProcessError if script fails
            # capture_output=False,
            # text=True,  # Capture output as string instead of bytes
            env=env,
        )
        # print("Script B ran successfully.")
        # print("Output:", result.stdout)
        run_success = True if result.returncode == 0 else False

    except subprocess.CalledProcessError as e:
        # print("Script B failed!")
        # print("Error Output:", e.stderr)
        run_success = False

    return run_success

###############################################################################
# Main script logic
#

__dirname__ = os.path.dirname(os.path.abspath(__file__))
script_paths = [
    f"{__dirname__}/basic.py",
    f"{__dirname__}/viewport_multiple.py",
    f"{__dirname__}/serialisation_json_cycle.py",
    f"{__dirname__}/serialisation_json_file.py",
]
for script_path in script_paths:
    # display the basename of the script without new line, and flush the output
    basename_script = basename(script_path)
    print(f"Running {basename_script} ... ", end="", flush=True)

    # launch the example script
    run_success = launch_example([sys.executable, script_path])

    # display X in red if failed, or a check in green if successful
    if run_success:
        print("\033[92mOK\033[0m")  # Green check mark
    else:
        print("\033[91mFailed\033[0m")  # Red X mark

    if not run_success:
        sys.exit(1)
