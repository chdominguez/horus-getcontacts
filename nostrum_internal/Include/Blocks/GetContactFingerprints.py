"""
Block for generating the frequencies
"""

from HorusAPI import PluginBlock, PluginVariable, VariableTypes

# INPUTS
freqs_input_variable = PluginVariable(
    id="frequencies_input",
    name="Frequencies TSV",
    description="Frequencies TSV",
    type=VariableTypes.FILE,
    allowedValues=["tsv"],
)

# VARIABLE
column_header_variable = PluginVariable(
    id="column_header",
    name="Structure name",
    description="The name of the structure to show as the header",
    type=VariableTypes.STRING,
    defaultValue="Structure",
)


def get_contact_fingerprints(block: PluginBlock):
    """
    Call the get_contact_fingerprints.py program
    """

    input_freqs_file = block.inputs[freqs_input_variable.id]
    header_name = block.variables[column_header_variable.id]

    from Utils.call_library import callLibrary

    command = "get_contact_fingerprints.py"
    args = (
        f"--input_frequencies {input_freqs_file}"
        + f" --column_headers {header_name}"
        + f" --flare_output {header_name}_multiflare.json"
        + f"--plot_output {header_name}_fingerprint.png"
    )

    callLibrary(command, args, block)


generate_contact_fingerprints_block = PluginBlock(
    id="generate_contact_fingerprints",
    name="Generate contact fingerprints",
    description="Generate a plot about the structure contacts",
    action=get_contact_fingerprints,
    inputs=[freqs_input_variable],
    variables=[column_header_variable],
)
