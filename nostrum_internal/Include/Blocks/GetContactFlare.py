"""
Block for generating the contact flare plot
"""

from HorusAPI import PluginBlock, PluginVariable, VariableTypes, Extensions

# INPUTS
contacts_input_variable = PluginVariable(
    id="contacts",
    name="Contacts TSV",
    description="The contacts TSV file",
    type=VariableTypes.FILE,
    allowedValues=["tsv"],
)

output_flare = PluginVariable(
    id="output_flare",
    name="Flare JSON",
    description="Flare plot JSON file",
    type=VariableTypes.FILE,
    allowedValues=["json"],
)


def generate_flareplot(block: PluginBlock):
    """
    Call the get_contact_flare.py program
    """

    contacts = block.inputs[contacts_input_variable.id]
    output_file = contacts.split(".")[0] + "_flare.json"

    from Utils.call_library import callLibrary

    command = "get_contact_flare.py"
    args = f"--input {contacts} --output {output_file}"

    callLibrary(command, args, block)

    block.setOutput(output_flare.id, output_file)

    with open(output_file, "r") as f:
        flareplotJSONData = f.read()

    Extensions().storeExtensionResults(
        pluginID="nostrum_internal",
        pageID="flareplot",
        data={"flareplotJSONData": flareplotJSONData},
        title="Flare plot",
    )


generate_flareplot_block = PluginBlock(
    id="generate_flareplot",
    name="Generate flare plot",
    description="Generate and visualize the flare plot of the structure",
    action=generate_flareplot,
    inputs=[contacts_input_variable],
    outputs=[output_flare],
)
