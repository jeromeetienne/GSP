import subprocess
import sys
import os


def launch_example(cmdline_args: list[str]) -> bool:
    """
    Launches the example script with the given command line arguments.

    :param cmdline_args: Command line arguments to run the script
    :type cmdline_args: list[str]
    :return: True if script ran successfully, False otherwise
    :rtype: bool
    """
    try:
        # Add a environment variable to disable interactive mode in the example
        env = dict(**os.environ, GSP_SC_INTERACTIVE="False")
        result = subprocess.run(
            cmdline_args,
            check=True,  # Raises CalledProcessError if script fails
            capture_output=True,
            text=True,
            env=env,
        )
        print("Script B ran successfully.")
        print("Output:", result.stdout)
        ran_success = True

    except subprocess.CalledProcessError as e:
        print("Script B failed!")
        print("Error Output:", e.stderr)
        ran_success = False

    return ran_success

def launch_pyright(script_path: str) -> bool:
    """
    Launches pyright on the given script path to check for type errors.

    :param script_path: Path to the script to check
    :type script_path: str
    :return: True if no type errors found, False otherwise
    :rtype: bool
    """
    try:
        result = subprocess.run(
            ["pyright", script_path],
            check=True,  # Raises CalledProcessError if pyright finds issues
            capture_output=True,
            text=True,
        )
        print("Pyright found no type errors.")
        print("Output:", result.stdout)
        type_check_success = True

    except subprocess.CalledProcessError as e:
        print("Pyright found type errors!")
        print("Error Output:", e.stderr)
        type_check_success = False

    return type_check_success

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
    run_success = launch_example([sys.executable, script_path])
    print("Example script ran successfully:", run_success)
    if not run_success:
        sys.exit(1)
    pyright_success = launch_pyright(script_path)
    print("Pyright type check passed:", pyright_success)
    if not pyright_success:
        sys.exit(1)