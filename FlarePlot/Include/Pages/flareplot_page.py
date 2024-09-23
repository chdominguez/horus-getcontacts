from HorusAPI import PluginPage, PluginEndpoint

flareplot_page = PluginPage(
    id="flareplot",
    name="Flare plot",
    description="Flare plot viewer",
    html="flare_view.html",
    hidden=True,
)


def fetch_flarefile():
    from flask import request, send_file

    file = request.args.get("flarefile")

    return send_file(file, as_attachment=True)


fetch_file_endpoint = PluginEndpoint(
    url="/api/flarefile",
    methods=["GET"],
    function=fetch_flarefile,
)

flareplot_page.addEndpoint(fetch_file_endpoint)
