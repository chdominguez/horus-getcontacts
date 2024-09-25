document.addEventListener("DOMContentLoaded", (e) => {
  setupFlarePlotAndFetchData();
});

let ALL_INTERACTIONS = [
  ["H-bond: sidechain - sidechain", "hbss"],
  ["H-bond: sidechain - backbone", "hbsb"],
  ["H-bond: backbone - backbone", "hbbb"],
  ["H-bond: ligand - sidechain", "hbls"],
  ["H-bond: ligand - backbone", "hblb"],
  ["H-bond: water mediated", "wb"],
  ["H-bond: extended water medid", "wb2"],
  ["H-bond: water mediated - ligand", "lwb"],
  ["H-bond: extended water mediated - ligand", "lwb2"],
  ["Salt bridge", "sb"],
  ["Salt bridge: ligand - protein", "sblp"],
  ["Salt bridge: protein - ligand", "sbpl"],
  ["Pi-cation", "pc"],
  ["Pi-stacking", "ps"],
  ["T-stacking", "ts"],
  ["Hydrophobic", "hp"],
  ["Hydrophobic: ligand - protein", "hplp"],
  ["van der Waals", "vdw"],
];

function getFlareDataFor(itype) {
  // Retrieve all of the interactions from the keys of the flareData
  // {
  //   "sb": {...},
  //   "hbss": {...},
  //   "vdw": {...}
  // }

  let newData = {};

  if (!itype) {
    // Then return all of them
    for (const i of Object.keys(window.flareData)) {
      newData = {
        ...window.flareData[i],
      };
    }
  } else {
    for (const i of Object.keys(window.flareData)) {
      if (itype.includes(i)) {
        newData = {
          ...window.flareData[i],
        };
      }
    }
  }

  return newData;
}

async function setupFlarePlotAndFetchData() {
  const jsonData = window.parent.extensionData["flareplotJSONData"];
  const loadingContainer = document.getElementById("loading-container");

  const fetchJsonData = () => fetchData(buildUrl(jsonData), loadingContainer);

  const parsedJsonData = await fetchJsonData()
    .then((data) => processData(data))
    .catch((err) => handleError(err, loadingContainer));

  // Store the data in the window object
  window.flareData = parsedJsonData;

  const interactions = Object.keys(parsedJsonData);

  // Filter the interactions to only show the ones that are in the flareData
  const filteredInteractions = ALL_INTERACTIONS.filter((a_i) =>
    interactions.includes(a_i[1])
  );

  setupInteractionSelector(filteredInteractions);

  const dataToShow = getFlareDataFor();

  setupFlareplot(dataToShow);

  function handleError(err, container) {
    container.innerHTML = "Error loading file: " + err;
  }
}

function buildUrl(jsonData, tsvFile) {
  const url = window.location.href + "api/flarefile";
  const parsedURL = new URL(url);
  parsedURL.searchParams.set("flarefile", jsonData);
  parsedURL.searchParams.set("tsvfile", tsvFile);
  return parsedURL.toString();
}

function fetchData(url, loadingContainer) {
  return fetch(url).then((response) => {
    const reader = response.body.getReader();
    const contentLength = +response.headers.get("Content-Length");
    let receivedLength = 0;
    let chunks = [];

    return new Promise((resolve, reject) => {
      function pump() {
        reader
          .read()
          .then(({ done, value }) => {
            if (done) {
              resolve(new Blob(chunks));
              return;
            }
            chunks.push(value);
            receivedLength += value.length;
            updateLoadingProgress(
              receivedLength,
              contentLength,
              loadingContainer
            );
            pump();
          })
          .catch(reject);
      }
      pump();
    });
  });
}

function updateLoadingProgress(
  receivedLength,
  contentLength,
  loadingContainer
) {
  const progress = Math.round((receivedLength / contentLength) * 100);
  loadingContainer.innerHTML = `Loading: ${progress}%`;

  if (progress === 100) {
    // Remove the loading container
    loadingContainer.remove();
  }
}

function processData(data) {
  return new Promise((resolve, reject) => {
    const fileReader = new FileReader();
    fileReader.onload = (e) => {
      try {
        const flareData = JSON.parse(e.target.result);
        resolve(flareData);
      } catch (error) {
        reject(new Error("Failed to parse JSON data"));
      }
    };
    fileReader.onerror = (error) => {
      reject(error);
    };
    fileReader.readAsText(data);
  });
}

function setupFlareplot(flareData) {
  const w = 340;

  // If exists, remove it
  if (document.getElementById("flare-container")) {
    document.getElementById("flare-container").remove();
  }

  const container = document.createElement("div");
  container.id = "flare-container";

  // Add the container after the itypeform
  document.getElementById("itypeform").after(container);

  const plot = createFlareplot(`${w}`, flareData, "#flare-container");

  setupResizing();

  plot.addNodeToggleListener(handleNodeToggle);

  const loadingContainer = document.getElementById("loading-container");
  loadingContainer?.remove();

  handleDynamics(plot);
}

async function handleNodeToggle(e) {
  const splitted = e.name.split(":");
  const resNum = Number(splitted[splitted.length - 1]);
  const chain = splitted[0];

  const firstStructure = parent.molstar.listStructures()[0];
  await parent.molstar.focus(firstStructure?.label, resNum, chain, 5);
}

function handleDynamics(plot) {
  const isDynamics = window.parent.extensionData["isDynamics"];
  if (!isDynamics) {
    document.getElementById("slider-container")?.remove();
  } else {
    // If exists, remove it
    if (document.getElementById("slider-container")) {
      document.getElementById("slider-container").remove();
    }

    const sliderContainer = document.createElement("div");
    sliderContainer.id = "slider-container";
    document.getElementById("flare-container").after(sliderContainer);

    createFlareplotSlider(plot, "#slider-container");
  }
}

function setupResizing() {
  const updateSize = () => {
    const parentWidth = window.innerWidth;
    const parentHeight = window.innerHeight - 150;
    const newScale = Math.min(parentWidth, parentHeight) / 360;

    const flareContainer = document.getElementById("flare-container");
    if (flareContainer) {
      flareContainer.style.transform = `scale(${newScale})`;
    } else {
      console.error("flare-container element not found");
    }
  };

  updateSize(); // Call once to set initial size

  // Remove the evenet listener if it exists
  window.removeEventListener("resize", updateSize);

  window.addEventListener("resize", updateSize);
}

function setupInteractionSelector(interactions, checkedInteractions) {
  // ---------------------------------------
  // Set up interaction selector
  // ---------------------------------------

  let interactionsToShow = interactions;
  if (!checkedInteractions) {
    // Select all
    interactionsToShow = interactions.map((i) => i[1]);
  }

  if (!window.ACTIVE_INTERACTIONS) {
    window.ACTIVE_INTERACTIONS = interactionsToShow;
  }

  const form = d3.select("#itypeform");
  interactions.forEach(function (itype, i) {
    const label = form.append("div").attr("class", "checkbox");

    label
      .append("input")
      .attr("type", "checkbox")
      .attr("id", "itypecheckbox_" + i)
      .attr("checked", interactionsToShow.includes(itype[1]))
      .on("change", function () {
        const interaction = itype[1];

        if (window.ACTIVE_INTERACTIONS.includes(interaction)) {
          window.ACTIVE_INTERACTIONS = window.ACTIVE_INTERACTIONS.filter(
            (i) => i !== interaction
          );
        } else {
          window.ACTIVE_INTERACTIONS.push(interaction);
        }

        const dataToShow = getFlareDataFor(window.ACTIVE_INTERACTIONS);
        setupFlareplot(dataToShow);
      });

    label
      .append("label")
      .attr("for", "itypecheckbox_" + i)
      .text(itype[0]);
  });
}
