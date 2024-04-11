from HorusAPI import PluginConfig, PluginVariable, VariableTypes
import os

conda_path_variable = PluginVariable(
    id="conda",
    name="conda executable",
    description="Path to the conda executable",
    defaultValue="conda",
    type=VariableTypes.FILE,
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
    variables=[conda_path_variable],
)
