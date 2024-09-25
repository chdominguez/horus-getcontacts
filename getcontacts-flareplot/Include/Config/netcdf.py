from HorusAPI import PluginConfig, PluginVariable, VariableTypes
import os

netcdf_path_variable = PluginVariable(
    id="netcdf",
    name="netcdf executable",
    description="Path to the netcdf executable",
    defaultValue="netcdf",
    type=VariableTypes.FILE,
)


def verify_netcdf(block: PluginConfig):
    path = block.variables["netcdf"]

    try:
        os.system(f"{path} --version")
    except Exception as e:
        raise Exception(
            f"Could not find netcdf on the following path: {path}. Error: {str(e)}"
        ) from e


netcdf_config_block = PluginConfig(
    name="netcdf path",
    description="Path to the netcdf executable",
    action=verify_netcdf,
    variables=[netcdf_path_variable],
)
