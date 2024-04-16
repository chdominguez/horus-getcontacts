from HorusAPI import PluginVariable, VariableTypes


# VARIABLES
cores = PluginVariable(
    id="cores",
    name="Cores",
    description="Number of CPU cores for parallelization",
    defaultValue=6,
    type=VariableTypes.NUMBER_RANGE,
    allowedValues=[1, 12, 1],
)

ligand = PluginVariable(
    id="ligand",
    name="Ligand",
    description="Resname of ligand molecule(s)",
    type=VariableTypes.STRING,
)

solvent = PluginVariable(
    id="solv",
    name="Solvent",
    description="The solvent, if any",
    type=VariableTypes.STRING,
)

vmd_sele_1 = PluginVariable(
    id="sele",
    name="Selection 1",
    description="VMD selection query to compute contacts in specified region of protein",
    defaultValue="protein",
    type=VariableTypes.STRING,
)

vmd_sele_2 = PluginVariable(
    id="sele2",
    name="Selection 2",
    description="Second VMD selection query to compute contacts between two regions of the protein",
    defaultValue=None,
    type=VariableTypes.STRING,
)

salt_bridges_variable = PluginVariable(
    id="sb",
    name="Salt bridges",
    description="Compute salt bridges interactions",
    type=VariableTypes.BOOLEAN,
    defaultValue=False,
    category="Interactions",
)

pi_cation_variable = PluginVariable(
    id="pc",
    name="π-cation",
    description="Compute π-cation interactions",
    type=VariableTypes.BOOLEAN,
    defaultValue=False,
    category="Interactions",
)

pi_stacking_variable = PluginVariable(
    id="ps",
    name="π-stacking",
    description="Compute π-stacking interactions",
    type=VariableTypes.BOOLEAN,
    defaultValue=False,
    category="Interactions",
)

ts_stacking_variable = PluginVariable(
    id="ts",
    name="T-stacking",
    description="Compute T-stacking interactions",
    type=VariableTypes.BOOLEAN,
    defaultValue=False,
    category="Interactions",
)

vdw_variable = PluginVariable(
    id="vdw",
    name="Van der Waals",
    description="Compute VdW interactions",
    type=VariableTypes.BOOLEAN,
    defaultValue=False,
    category="Interactions",
)

# Hydrogen bond

hb_variable = PluginVariable(
    id="hb",
    name="Hydrogen bonds",
    description="Compute hydrogen bond interactions. This will compute all H-Bond interactions.",
    type=VariableTypes.BOOLEAN,
    defaultValue=True,
    category="H-bond",
)

hbbb_variable = PluginVariable(
    id="hbbb",
    name="Backbone-backbone hydrogen bonds",
    description="Compute backbone-backbone hydrogen bond interactions.",
    type=VariableTypes.BOOLEAN,
    defaultValue=False,
    category="H-bond",
)

hbsb_variable = PluginVariable(
    id="hbsb",
    name="Backbone-sidechain hydrogen bonds",
    description="Compute backbone-sidechain hydrogen bond interactions.",
    type=VariableTypes.BOOLEAN,
    defaultValue=False,
    category="H-bond",
)

hbss_variable = PluginVariable(
    id="hbss",
    name="Sidechain-sidechain hydrogen bonds",
    description="Compute sidechain-sidechain hydrogen bond interactions.",
    type=VariableTypes.BOOLEAN,
    defaultValue=False,
    category="H-bond",
)

wb_variable = PluginVariable(
    id="wb",
    name="Water-mediated hydrogen bond",
    description="Compute water-mediated hydrogen bond interactions.",
    type=VariableTypes.BOOLEAN,
    defaultValue=False,
    category="H-bond",
)

wb2_variable = PluginVariable(
    id="wb2",
    name="Extended water-mediated hydrogen bond",
    description="Compute extended water-mediated hydrogen bond interactions.",
    type=VariableTypes.BOOLEAN,
    defaultValue=False,
    category="H-bond",
)

hblb_variable = PluginVariable(
    id="hblb",
    name="Ligand-backbone hydrogen bonds",
    description="Compute ligand-backbone hydrogen bond interactions.",
    type=VariableTypes.BOOLEAN,
    defaultValue=False,
    category="H-bond",
)

hbls_variable = PluginVariable(
    id="hbls",
    name="Ligand-sidechain hydrogen bonds",
    description="Compute ligand-sidechain hydrogen bond interactions.",
    type=VariableTypes.BOOLEAN,
    defaultValue=False,
    category="H-bond",
)

lwb_variable = PluginVariable(
    id="lwb",
    name="Ligand water-mediated hydrogen bond",
    description="Compute ligand water-mediated hydrogen bond interactions.",
    type=VariableTypes.BOOLEAN,
    defaultValue=False,
    category="H-bond",
)

lwb2_variable = PluginVariable(
    id="lwb2",
    name="Ligand extended water-mediated hydrogen bond",
    description="Compute ligand extended water-mediated hydrogen bond interactions.",
    type=VariableTypes.BOOLEAN,
    defaultValue=False,
    category="H-bond",
)

all_itypes = [
    salt_bridges_variable,
    pi_cation_variable,
    pi_stacking_variable,
    ts_stacking_variable,
    vdw_variable,
    hb_variable,
    hbbb_variable,
    hbsb_variable,
    hbss_variable,
    wb_variable,
    wb2_variable,
    hblb_variable,
    hbls_variable,
    lwb_variable,
    lwb2_variable,
]

general_variables = [cores, solvent, ligand, vmd_sele_1, vmd_sele_2]

all_variables = general_variables + all_itypes
