"""
Wrapper for calling the module library
"""

import subprocess
import sys
import os
from HorusAPI import PluginBlock


def callLibrary(command: str, args: str, block: PluginBlock):
    """
    Will run the command on the right path
    """

    # Get the plugin path from the include
    module_path = ""
    for path in sys.path:
        if "Include" in path:
            module_path = path

    conda_path = block.config["conda"]
    command = os.path.join(module_path, "getcontacts", command)

    # Read the license file
    license = ""
    with open(os.path.join(module_path, "LICENSE")) as f:
        license = f.read()

    print(license)

    with subprocess.Popen(
        f"{conda_path} run -n nostrum_internal_plugin python '{command}' {args}",
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,  # Ensure text mode for Python 3
    ) as p:
        # Print the output
        if p.stdout is None:
            raise Exception("Could not get the output of the script.")

        for line in p.stdout:
            strippedOut = line.strip()
            if strippedOut != "":
                print(strippedOut)

        # Print the error
        if p.stderr:
            for line in p.stderr:
                strippedErr = line.strip()
                if strippedErr != "":
                    print(strippedErr)

        # Wait for the process to finish
        p.wait()

        # Check the return code
        if p.returncode != 0 and p.returncode is not None:
            raise Exception(f"Script failed. Check the Horus console")
