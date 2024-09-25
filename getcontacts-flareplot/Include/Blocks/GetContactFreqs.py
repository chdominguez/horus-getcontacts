"""
Block for generating the frequencies
"""

from HorusAPI import PluginBlock, PluginVariable, VariableTypes

# INPUTS
contacts_input_variable = PluginVariable(
    id="contacts",
    name="Contacts TSV",
    description="The contacts TSV file",
    type=VariableTypes.FILE,
    allowedValues=["tsv"],
)

labels_input_variable = PluginVariable(
    id="labels",
    name="Labels TSV",
    description="The labels TSV file",
    type=VariableTypes.FILE,
    allowedValues=["tsv"],
)

output_tsv = PluginVariable(
    id="output_tsv",
    name="Frequencies TSV",
    description="Contact map",
    type=VariableTypes.FILE,
    allowedValues=["tsv"],
)


def generate_freqs(block: PluginBlock):
    """
    Call the generate_contact_frequencies.py program
    """

    contacts = block.inputs["contacts"]
    labels = block.inputs["labels"]
    output_file = contacts + "_freqs.tsv"

    from Utils.call_library import callLibrary

    command = "get_contact_frequencies.py"
    args = f"--input_files {contacts} --label_file {labels} --itypes all --output_file {output_file}"

    callLibrary(command, args, block)

    block.setOutput(output_tsv.id, output_file)


generate_freqs_block = PluginBlock(
    id="generate_contact_frequencies",
    name="Generate contact frequencies",
    description="Generate a frequencies map for a given structure",
    action=generate_freqs,
    inputs=[contacts_input_variable, labels_input_variable],
    outputs=[output_tsv],
)
