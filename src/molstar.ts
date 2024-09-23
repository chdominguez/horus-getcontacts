import { StructureSelection } from "molstar/lib/mol-model/structure";
import { createStructureRepresentationParams } from "molstar/lib/mol-plugin-state/helpers/structure-representation-params";
import { StructureRef } from "molstar/lib/mol-plugin-state/manager/structure/hierarchy-state";
import { PluginStateObject } from "molstar/lib/mol-plugin-state/objects";
import { StateTransforms } from "molstar/lib/mol-plugin-state/transforms";
import { PluginUIContext } from "molstar/lib/mol-plugin-ui/context";
import { PluginCommands } from "molstar/lib/mol-plugin/commands";
import { MolScriptBuilder as MS } from "molstar/lib/mol-script/language/builder";
import { Expression } from "molstar/lib/mol-script/language/expression";
import { Script } from "molstar/lib/mol-script/script";
import { State } from "molstar/lib/mol-state";

export type MolInfo = {
  id: string;
  label: string;
  fileContents: string;
  fileName: string;
  format: string;
};

export type AtomInfo = {
  name: string;
  residue: number;
  chainID: string;
  atom_index: number;
  auth_comp_id: string;
  auth_atom_id: string;
  type: string;
  x: number;
  y: number;
  z: number;
  label: string;
  structureID?: string;
};

declare global {
  interface Window {
    molstar: {
      getStructureFromModelID: (id: string) => StructureRef | null;
      getStructureObjectFromLabel: (label: string) => StructureRef | null;
      getStructureIDFromStructureRef: (
        structureRef: StructureRef
      ) => string | null;
      listStructures: () => MolInfo[];
      plugin: PluginUIContext;
      focus: (label: string, seq?: number, chain?: string) => void;
      state: State;
      listChains: (structureLabel?: string) => AtomInfo[];
    };
  }
}

type Residue = {
  seq: number;
  chain?: string;
  structureLabel?: string;
};

const GROUP_LABEL = "selection";
const TRANSFORM_LABEL = "selection-group";

export async function focusResidue(residue: Residue) {
  const { seq, chain } = residue;

  const structureLabel = parent.molstar.listStructures()[0]?.label;

  if (!structureLabel) {
    alert("No structure loaded");
    return "No structure loaded";
  }

  parent.molstar.focus(structureLabel, residue.seq, residue.chain);

  const plugin = parent.molstar.plugin;
  const state = plugin.state.data;

  // Assume we have only one structure
  const structures = parent.molstar.listStructures();

  if (structures.length === 0) {
    alert("No structures to focus found.");
    return;
  }

  const structure = structures[0];

  // parent.molstar.focus(structure.label, seq, chain);

  const structureRef = parent.molstar.getStructureObjectFromLabel(
    structure.label
  );

  if (!structureRef) {
    return "Internal error: No suitable model found";
  }

  // Select the model where we will place the new focus group
  const modelKey = parent.molstar.getStructureIDFromStructureRef(structureRef);

  if (!modelKey) {
    return " Internal error: No suitable model found";
  }

  const model = state.select(modelKey)[0]!
    .obj as PluginStateObject.Molecule.Structure;

  // Get the 'Update' object from Mol*. This is used to update the state of the visualizer
  const update = state.build();

  // Delete any previous selections
  update.delete(GROUP_LABEL);

  // Define a label for the new selection, this will appear on the Mol* state tree
  const focusLabel = `Focus - ${chain}:${seq}`;

  // Get the residue from the provided resdiue number
  // We define a filter group. This will tell Mol* to filter the structure and only keep the residues that match the filter
  const filterGroups: Record<string, Expression> = {
    "residue-test": MS.core.rel.eq([
      MS.struct.atomProperty.macromolecular.auth_seq_id(),
      seq,
    ]),
    "chain-test": MS.core.rel.eq([
      MS.struct.atomProperty.macromolecular.auth_asym_id(),
      chain || "A",
    ]),
  };

  // We call the filter function to filter the structure and obtain the first residue that matches the filter
  const filteredResidue = MS.struct.filter.first([
    MS.struct.generator.atomGroups(filterGroups),
  ]);

  // Now we will add, under the desired structure tree, a new model for the selection
  // We use the update object to add a new model to the structure tree. We assign to this
  // model the label we defined earlier and a reference to the selection object, so later
  // we can use it to create a representation or to delete it
  const group = update
    .to(modelKey)
    .group(
      StateTransforms.Misc.CreateGroup,
      { label: focusLabel },
      { ref: GROUP_LABEL }
    );

  // Inside the new group named 'Focus' we create the actual residue selection
  // We assign to it the SelectionGroup too
  const filteredResidueInner = group.apply(
    StateTransforms.Model.StructureSelectionFromExpression,
    { label: focusLabel, expression: filteredResidue },
    { ref: TRANSFORM_LABEL }
  );

  // To our new selection, we add a representation based on the data of the structure
  // We assing the ball-and-stick representation to the selection, so we can see the residue's atoms
  filteredResidueInner.apply(
    StateTransforms.Representation.StructureRepresentation3D,
    createStructureRepresentationParams(plugin, model.data, {
      type: "ball-and-stick",
    })
  );

  // We will apply a modifier to the selection, to include the surroundings of the residue
  const surroundings = MS.struct.modifier.includeSurroundings({
    0: filteredResidue,
    radius: 5,
    "as-whole-residues": true,
  });

  // Then, to the existing group, we will add a new selection which represents the surroundings
  group
    .apply(StateTransforms.Model.StructureSelectionFromExpression, {
      label: "Surroundings",
      expression: surroundings,
    })
    .apply(
      StateTransforms.Representation.StructureRepresentation3D,
      createStructureRepresentationParams(plugin, model.data, {
        type: "ball-and-stick",
      })
    );

  // Get a loci from the expression
  const loci = StructureSelection.toLociWithSourceUnits(
    Script.getStructureSelection(filteredResidue, model.data)
  );

  plugin.managers.camera.focusLoci(loci);

  await PluginCommands.State.Update(plugin, {
    state: state,
    tree: update,
  });

  return "Residue focused";
}
