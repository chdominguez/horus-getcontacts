from HorusAPI import PluginConfig, PluginVariable, VariableTypes
import os

conda_path_variable = PluginVariable(
    id="conda",
    name="conda executable",
    description="Path to the conda executable",
    defaultValue="conda",
    type=VariableTypes.FILE,
)

conda_env_name_variable = PluginVariable(
    id="conda_env",
    name="conda environment",
    description="Name of the conda environment with the get_contacts package installed.",
    defaultValue="get_contacts_horus",
    type=VariableTypes.STRING,
)


def verify_conda(block: PluginConfig):
    path = block.variables["conda"]

    try:
        os.system(f"{path} --version")
    except Exception as e:
        raise Exception(
            f"Could not find conda on the following path: {path}. Error: {str(e)}"
        ) from e


conda_config_block = PluginConfig(
    name="conda path",
    description="Path to the conda executable",
    action=verify_conda,
    variables=[conda_path_variable, conda_env_name_variable],
)
