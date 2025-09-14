from posixpath import basename
import subprocess
import sys
import os
from time import sleep

__dirname__ = os.path.dirname(os.path.abspath(__file__))

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
            capture_output=True,
            text=True,  # Capture output as string instead of bytes
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

def launch_network_server():
    """
    Launches the network server in a separate process.

    Returns:
        The subprocess.Popen object representing the server process.
    """
    try:
        # Add a environment variable to disable interactive mode in the example
        env = dict(**os.environ, GSP_SC_INTERACTIVE="False")

        server_process = subprocess.Popen(
            [sys.executable, f"{__dirname__}/network_server.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,  # Capture output as string instead of bytes
            env=env,
        )
        print("Network server started.")
        return server_process

    except Exception as e:
        print("Failed to start network server:", str(e))
        return None
###############################################################################
# Main script logic
#

def main()->None:
    # Launch the network server
    server_process = launch_network_server()
    if not server_process:
        sys.exit(1)

    script_paths = [
        f"{__dirname__}/basic.py",
        f"{__dirname__}/viewport_multiple.py",
        f"{__dirname__}/serialisation_json_cycle.py",
        f"{__dirname__}/serialisation_json_file.py",
        f"{__dirname__}/network_client.py",
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

    # Terminate the server process
    server_process.terminate()
    server_process.wait()
    print("Network server terminated.")

if __name__ == "__main__":
    main()