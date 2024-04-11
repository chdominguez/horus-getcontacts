import os
from HorusAPI import PluginBlock, PluginVariable, VariableTypes, Extensions

# INPUTS
topology_input_variable = PluginVariable(
    id="topology",
    name="Topology PDB",
    description="The topology PDB file to compute its contacts",
    type=VariableTypes.STRUCTURE,
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
    args = f"--topology {structure_path} --trajectory {trajectory_path} --itypes all --output {output_file}"

    from Utils.call_library import callLibrary

    callLibrary(command, args, block)

    block.setOutput(output_tsv.id, output_file)


generate_dynamic_contacts_block = PluginBlock(
    id="generate_dynamic_contacts",
    name="Get dynamic contacts",
    description="Generate a dybamic contact map for a given simulation",
    action=generate_dynamic_contacts,
    inputs=[topology_input_variable, trajectory_input_variable],
    outputs=[output_tsv],
)
