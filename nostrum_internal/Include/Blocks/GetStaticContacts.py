import os
from HorusAPI import PluginBlock, PluginVariable, VariableTypes, Extensions

# INPUTS
topology_input_variable = PluginVariable(
    id="topology",
    name="Topology PDB",
    description="The topology PDB file to compute its contacts",
    type=VariableTypes.STRUCTURE,
)

# VARIABLES

salt_bridges_variable = PluginVariable(
    id="salt_bridges",
    name="Salt bridges",
    description="Compute salt bridges interactions",
    type=VariableTypes.BOOLEAN,
    defaultValue=False,
)

pi_cation_variable = PluginVariable(
    id="pi_cation",
    name="π-cation",
    description="Compute π-cation interactions",
    type=VariableTypes.BOOLEAN,
    defaultValue=False,
)

pi_stacking_variable = PluginVariable(
    id="pi_stacking",
    name="π-stacking",
    description="Compute π-stacking interactions",
    type=VariableTypes.BOOLEAN,
    defaultValue=False,
)

ts_stacking_variable = PluginVariable(
    id="ts_stacking",
    name="T-stacking",
    description="Compute T-stacking interactions",
    type=VariableTypes.BOOLEAN,
    defaultValue=False,
)

vdw_variable = PluginVariable(
    id="vdw",
    name="Van der Waals",
    description="Compute VdW interactions",
    type=VariableTypes.BOOLEAN,
    defaultValue=False,
)

hb_variable = PluginVariable(
    id="hb",
    name="Hydrogen bonds",
    description="Compute hydrogen bond interactions",
    type=VariableTypes.BOOLEAN,
    defaultValue=True,
)

output_tsv = PluginVariable(
    id="output_tsv",
    name="Contacts TSV",
    description="Contact map",
    type=VariableTypes.FILE,
    allowedValues=["tsv"],
)


def generate_contacts(block: PluginBlock):
    structure_path = block.inputs["topology"]
    structure_name = os.path.basename(structure_path).split(".")[0]
    output_file = structure_name + "_contacts.tsv"

    command = "get_static_contacts.py"
    args = f"--structure {structure_path} --itypes all --output {output_file}"

    from Utils.call_library import callLibrary

    callLibrary(command, args, block)

    block.setOutput(output_tsv.id, output_file)


get_contacts_block = PluginBlock(
    id="get_static_contacts",
    name="Get static contacts",
    description="Generate a static contact map for a given structure",
    action=generate_contacts,
    inputs=[topology_input_variable],
    variables=[
        hb_variable,
        salt_bridges_variable,
        pi_cation_variable,
        pi_stacking_variable,
        ts_stacking_variable,
        vdw_variable,
    ],
    outputs=[output_tsv],
)
