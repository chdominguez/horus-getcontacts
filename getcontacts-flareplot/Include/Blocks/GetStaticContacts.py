import os
from HorusAPI import PluginBlock, PluginVariable, VariableTypes
from Utils.arguments import all_variables, all_itypes, general_variables

# INPUTS
topology_input_variable = PluginVariable(
    id="topology",
    name="Topology PDB",
    description="The topology PDB file to compute its contacts",
    type=VariableTypes.FILE,
    allowedValues=["pdb"],
)

output_tsv = PluginVariable(
    id="output_tsv",
    name="Contacts TSV",
    description="Contact map",
    type=VariableTypes.FILE,
    allowedValues=["tsv"],
)

parsed_general_variables = []
for variable in general_variables:
    if variable.id in ["cores", "solv"]:
        continue
    parsed_general_variables.append(variable)


def generate_contacts(block: PluginBlock):
    structure_path = block.inputs["topology"]
    structure_name = os.path.basename(structure_path).split(".")[0]
    output_file = structure_name + "_contacts.tsv"

    command = "get_static_contacts.py"
    args = f"--structure {structure_path} --output {output_file}"

    # Add to the args the block variables and the itypes
    itypes = " --itypes"
    for v in all_itypes:
        if block.variables[v.id] == True:
            itypes += f" {v.id}"

    args += itypes

    general_values = ""
    for variable in parsed_general_variables:
        value = block.variables.get(variable.id)  # Getting the value or None if not set
        if value is not None:
            if variable.id.startswith("sele"):
                general_values += f' --{variable.id} "{value}"'
            else:
                general_values += f" --{variable.id} {value}"

    args += general_values

    # Parse additional commands if necessary

    from Utils.call_library import callLibrary

    callLibrary(command, args, block)

    block.setOutput(output_tsv.id, output_file)


# For the get static contacts remove the cores and solvent arguments

get_contacts_block = PluginBlock(
    id="get_static_contacts",
    name="Get static contacts",
    description="Generate a static contact map for a given structure",
    action=generate_contacts,
    inputs=[topology_input_variable],
    variables=parsed_general_variables + all_itypes,
    outputs=[output_tsv],
)
