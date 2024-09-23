import os
from HorusAPI import PluginBlock, PluginVariable, VariableTypes, Extensions
from Utils.arguments import all_variables, all_itypes, general_variables

# INPUTS
topology_input_variable = PluginVariable(
    id="topology",
    name="Topology PDB",
    description="The topology PDB file to compute its contacts",
    type=VariableTypes.FILE,
    allowedValues=["pdb"],
)

trajectory_input_variable = PluginVariable(
    id="trajectory",
    name="Trajectory",
    description="The trajectory file from the simulation",
    type=VariableTypes.FILE,
    allowedValues=["nc", "xtc", "dcd"],
)

output_tsv = PluginVariable(
    id="output_tsv",
    name="Contacts TSV",
    description="Contact map",
    type=VariableTypes.FILE,
    allowedValues=["tsv"],
)


def generate_dynamic_contacts(block: PluginBlock):
    structure_path = block.inputs["topology"]
    structure_name = os.path.basename(structure_path).split(".")[0]
    trajectory_path = block.inputs["trajectory"]
    output_file = structure_name + "_contacts.tsv"

    command = "get_dynamic_contacts.py"
    args = f"--topology {structure_path} --trajectory {trajectory_path} --output {output_file}"

    # Add to the args the block variables and the itypes
    itypes = " --itypes"
    for v in all_itypes:
        if block.variables[v.id] == True:
            itypes += f" {v.id}"

    args += itypes

    general_values = ""
    for variable in general_variables:
        value = block.variables.get(variable.id)  # Getting the value or None if not set
        if value is not None:
            if variable.id.startswith("sele"):
                general_values += f" --{variable.id} '{value}'"
            else:
                general_values += f" --{variable.id} {value}"

    args += general_values

    from Utils.call_library import callLibrary

    callLibrary(command, args, block)

    block.setOutput(output_tsv.id, output_file)


generate_dynamic_contacts_block = PluginBlock(
    id="generate_dynamic_contacts",
    name="Get dynamic contacts",
    description="Generate a dynamic contact map for a given simulation",
    action=generate_dynamic_contacts,
    inputs=[topology_input_variable, trajectory_input_variable],
    variables=all_variables,
    outputs=[output_tsv],
)
