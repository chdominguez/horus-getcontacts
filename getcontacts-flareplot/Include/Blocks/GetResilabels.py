"""
Block for generating the residue labels
"""

from HorusAPI import PluginBlock, PluginVariable, VariableTypes

# INPUTS
xml_input_variable = PluginVariable(
    id="xml_input",
    name="PDBeFold XML",
    description="PDBeFold XML generated with www.ebi.ac.uk/msd-srv/ssm/",
    type=VariableTypes.FILE,
    allowedValues=["xml"],
)

output_tsv = PluginVariable(
    id="output_labels",
    name="Residue labels",
    description="The residue labels produced by the get_resilabels program",
    type=VariableTypes.FILE,
    allowedValues=["tsv"],
)


def generate_resilabels(block: PluginBlock):
    """
    Call the generate_resilabels.py program
    """

    xml_input = block.inputs["xml_input"]
    output_prefix = "labels_" + xml_input
    output_filename = output_prefix + ".tsv"

    from Utils.call_library import callLibrary

    command = "get_resilabels.py"
    args = f"--input_files {xml_input} --output_prefix {output_prefix}"

    callLibrary(command, args, block)

    block.setOutput(output_tsv.id, output_filename)


generate_resilabels_block = PluginBlock(
    id="get_resilabels",
    name="Generate residue labels",
    description="Generate the residue labels file from a given PDBeFold XML file",
    action=generate_resilabels,
    inputs=[xml_input_variable],
    outputs=[output_tsv],
)
