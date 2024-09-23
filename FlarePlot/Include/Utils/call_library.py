"""
Wrapper for calling the module library
"""

import subprocess
import os
from HorusAPI import PluginBlock

from Config.conda import conda_env_name_variable, conda_path_variable


def callLibrary(command: str, args: str, block: PluginBlock):
    """
    Will run the command on the right path
    """

    # Get the plugin path from the include
    include_path = os.path.join(block.pluginDir, "Include")

    # Get the environment name and conda path
    env_name = block.config[conda_env_name_variable.id]
    conda_path = block.config[conda_path_variable.id]
    command = os.path.join(include_path, "getcontacts", command)

    # Read the license file
    license = ""
    with open(os.path.join(include_path, "getcontacts", "LICENSE")) as f:
        license = f.read()

    print(license)
    print(
        "command: ",
        f"{conda_path} run -n {env_name} python '{command}' {args}",
    )
    with subprocess.Popen(
        f"{conda_path} run -n {env_name} python '{command}' {args}",
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
