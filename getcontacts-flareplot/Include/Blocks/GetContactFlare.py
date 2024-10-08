"""
Block for generating the contact flare plot
"""

import os
import json

from HorusAPI import (
    PluginBlock,
    PluginVariable,
    VariableTypes,
    Extensions,
    VariableList,
)

# INPUTS
contacts_input_variable = PluginVariable(
    id="contacts",
    name="Contacts TSV",
    description="The contacts TSV file",
    type=VariableTypes.FILE,
    allowedValues=["tsv"],
)

reslabel_chain = PluginVariable(
    id="reslabel_chain",
    name="Chain",
    description="The chain of the residue",
    type=VariableTypes.STRING,
)

reslabel_restype = PluginVariable(
    id="reslabel_start",
    name="Start residue",
    description="The starting residue number",
    type=VariableTypes.STRING,
)

reslabel_resid = PluginVariable(
    id="reslabel_final",
    name="Final residue",
    description="The number of the residue",
    type=VariableTypes.NUMBER,
)

reslabel_label = PluginVariable(
    id="reslabel_label",
    name="Label",
    description="The label to use for the residue",
    type=VariableTypes.STRING,
)

reslabel_color = PluginVariable(
    id="reslabel_color",
    name="Color",
    description="The color of the residue",
    type=VariableTypes.STRING_LIST,
    allowedValues=["red", "blue", "yellow", "orange", "purple", "green"],
)

reslabels = VariableList(
    id="reslabels",
    name="Residue labels",
    description="Used to decorate the flareplot with colors and edge-bundling",
    prototypes=[
        reslabel_chain,
        reslabel_restype,
        reslabel_resid,
        reslabel_label,
        reslabel_color,
    ],
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
    reslabels_value = block.variables[reslabels.id]

    # Read the TSV file to get the unique itypes (2nd column)
    itypes = set()
    with open(contacts, "r") as f:
        for line in f:
            if line.startswith("#"):
                continue
            splitted_line = line.split("\t")
            itypes.add(splitted_line[1])

    itypes = list(itypes)

    job_name = contacts.split(".")[0]

    command = "get_contact_flare.py"
    args = f"--input {contacts}"

    if reslabels_value is not None:

        # First we need to get all of the existing contacts form the contatcs.tsv file
        all_residues = []
        with open(contacts, "r") as f:
            contacts_contents = f.readlines()

            for line in contacts_contents:
                if line.startswith("#"):
                    continue
                splitted_line = line.split("\t")
                residue = splitted_line[2]
                splitted_residue = ":".join(residue.split(":")[:-1])
                if splitted_residue not in all_residues:
                    all_residues.append(splitted_residue)

                residue = splitted_line[3]
                splitted_residue = ":".join(residue.split(":")[:-1])
                if splitted_residue not in all_residues:
                    all_residues.append(splitted_residue)

        flarelabels_file = f"{job_name}_labels.tsv"
        # Write the TSV file with all the variables
        with open(flarelabels_file, "w") as f:
            lines = ""
            for rl in reslabels_value:
                chain = rl["reslabel_chain"]
                res_start = int(rl["reslabel_start"])
                res_final = (
                    int(rl["reslabel_final"]) + 1  # +1 for range to work correctly
                )
                label = rl["reslabel_label"]
                color = rl["reslabel_color"]
                for i in range(res_start, res_final):
                    res_type = None
                    for r in all_residues:
                        rtype = r.split(":")[1]
                        rid = int(r.split(":")[-1])
                        if rid == i:
                            res_type = rtype

                    if res_type is None:
                        raise Exception(f"Could not infer residue type for res:{i}")
                    residue_string = f"{chain}:{res_type}:{i}"
                    if label is None:
                        parsed_label = residue_string
                    else:
                        parsed_label = label + f":{i}"
                    if residue_string in all_residues:
                        all_residues.remove(residue_string)

                    line = f"{residue_string}\t{parsed_label}\t{color}\n"
                    lines += line

            # Write labeled residues
            f.write(lines)

            # Write rest of them
            for line in all_residues:
                f.write(f"{line}\t{line}\t#FFFFFF00\n")

        args += f" --flarelabels {flarelabels_file}"

    # Generate a list of args for each itype
    flareplot_dict = {}
    for i in range(len(itypes)):
        itype = itypes[i]
        output_tmp_file = f"{job_name}_{itype}_flare.json"
        current_args = args + f" --itype {itype} --output {output_tmp_file}"

        print(f"Generating flareplot for itype: {itype} ")

        from Utils.call_library import callLibrary

        callLibrary(command, current_args, block, print_license=i == 0)

        # Read the flareplot file
        with open(output_tmp_file, "r") as f:
            flareplot_dict[itype] = json.load(f)

        os.remove(output_tmp_file)

    global_flareplot_file = f"{job_name}_flareplot.json"
    # Write the flareplot dictionary to a JSON file
    with open(global_flareplot_file, "w") as f:
        json.dump(flareplot_dict, f)

    block.setOutput(output_flare.id, global_flareplot_file)

    is_dynamics = False

    # Read the tsv file first line to check the total_frames
    with open(contacts, "r") as f:
        first_line = f.readline()
        if "total_frames:1" in first_line:
            is_dynamics = False
        else:
            is_dynamics = True

    Extensions().storeExtensionResults(
        pluginID="getcontacts_flareplot",
        pageID="flareplot",
        data={
            "tsvFile": os.path.abspath(contacts),
            "flareplotJSONData": os.path.abspath(global_flareplot_file),
            "isDynamics": is_dynamics,
        },
        title="Flare plot",
    )


generate_flareplot_block = PluginBlock(
    id="generate_flareplot",
    name="Generate flare plot",
    description="Generate and visualize the flare plot of the structure",
    action=generate_flareplot,
    inputs=[contacts_input_variable],
    variables=[reslabels],
    outputs=[output_flare],
)
