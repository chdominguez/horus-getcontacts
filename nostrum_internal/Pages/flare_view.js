
document.addEventListener("DOMContentLoaded", (e) => {

    const jsonData = window.parent.extensionData["flareplotJSONData"];
    const flareData = JSON.parse(jsonData);

    // Get window size
    const w = window.parent.innerWidth / 3;

    const plot = createFlareplot(`${w}`, flareData, "#flare-container");
    createFlareplotSlider(plot, "#slider-container");

    plot.addNodeToggleListener(async (e) => {
        // Get chain and residue number
        const splitted = e.name.split(":");
        const chain = splitted[0];
        const resNum = Number(splitted[2]);
        result = await parent.molstar.focus(undefined, resNum);
    });
})