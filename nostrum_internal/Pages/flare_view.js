
document.addEventListener("DOMContentLoaded", (e) => {

    const jsonData = window.parent.extensionData["flareplotJSONData"];
    const flareData = JSON.parse(jsonData);

    // Get window size
    const w = window.parent.innerWidth / 3;

    const plot = createFlareplot(`${w}`, flareData, "#flare-container");
    createFlareplotSlider(plot, "#slider-container");

    plot.addNodeToggleListener(async (e) => {
        // Get residue number
        const splitted = e.name.split(":");
        const resNum = Number(splitted[splitted.length - 1]);
        result = await parent.molstar.focus(undefined, resNum);
    });
})