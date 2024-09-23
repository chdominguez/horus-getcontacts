document.addEventListener("DOMContentLoaded", (e) => {
  const jsonData = window.parent.extensionData["flareplotJSONData"];
  const isDynamics = window.parent.extensionData["isDynamics"];

  // Fetch the file
  var url = window.location.href + "api/flarefile";

  // Add the flarefile path to the url
  const parsedURL = new URL(url);
  parsedURL.searchParams.set("flarefile", jsonData);
  url = parsedURL.toString();

  const loadingContainer = document.getElementById("loading-container");

  // Fetch it
  fetch(url)
    .then((response) => {
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
              const progress = Math.round(
                (receivedLength / contentLength) * 100
              );
              loadingContainer.innerHTML = `Loading: ${progress}%`;
              pump();
            })
            .catch(reject);
        }
        pump();
      });
    })
    .then((data) => {
      // Load the file
      const fileReader = new FileReader();
      fileReader.onload = (e) => {
        const flareData = e.target.result;

        // Get window size
        // const w = window.parent.innerWidth / 3;
        const w = 340;
        const plot = createFlareplot(`${w}`, flareData, "#flare-container");
        createFlareplotSlider(plot, "#slider-container");

        plot.addNodeToggleListener(async (e) => {
          // Get residue number
          const splitted = e.name.split(":");
          const resNum = Number(splitted[splitted.length - 1]);
          const chain = splitted[0];

          // focusResidue(residue)
          //   .then((msg) => console.log(msg))
          //   .catch((error) => console.error(error));

          // Focus the residue
          const firstStructure = parent.molstar.listStructures()[0];
          await parent.molstar.focus(firstStructure?.label, resNum, chain, 5);
        });

        loadingContainer.remove();

        // If its not dynamics, remove the slider
        if (!isDynamics) {
          document.getElementById("slider-container").remove();
        }

        const updateSize = () => {
          const parentWidth = window.innerWidth;
          const parentHeight = window.innerHeight;
          const newScale = Math.min(parentWidth, parentHeight) / 360;
          document.getElementById(
            "div-container"
          ).style.transform = `scale(${newScale})`;
        };

        updateSize();

        // Add resize event listener
        window.addEventListener("resize", () => {
          updateSize();
        });
      };

      fileReader.readAsText(data);
    })
    .catch((err) => {
      loadingContainer.innerHTML = "Error loading file: " + err;
    });
});
