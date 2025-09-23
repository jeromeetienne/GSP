"""
Server example using Flask to render a scene from JSON input.

- use Flask to create a simple web server
- render with matplotlib
"""

from flask import Flask, request, send_file, Response
import io
import argparse
import gsp_sc.src as gsp_sc

flask_app = Flask(__name__)


@flask_app.route("/render_scene", methods=["POST"])
def render_scene_json() -> Response:
    scene_json = request.get_json()

    ###############################################################################
    # Load the scene from JSON
    #
    json_parser = gsp_sc.renderer.json.JsonParser()
    canvas_parsed, camera_parsed = json_parser.parse(scene_json)

    ###############################################################################
    # Render the loaded scene with matplotlib
    #
    matplotlib_renderer = gsp_sc.renderer.matplotlib.MatplotlibRenderer()
    image_png_data = matplotlib_renderer.render(
        canvas=canvas_parsed, camera=camera_parsed, show_image=False
    )

    ###############################################################################
    # Return the rendered image as a PNG file
    #
    return send_file(
        io.BytesIO(image_png_data),
        mimetype="image/png",
        as_attachment=True,
        download_name="rendered_scene.png",
    )


#######################################################################################

if __name__ == "__main__":

    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Run the network server for rendering. see ./examples/network_client.py for usage.")
    args = parser.parse_args()

    flask_app.run(threaded=False, debug=False)  # Enable debug mode if desired
