from flask import Flask, jsonify, request, send_file
import io
import gsp_sc.src as gsp_sc

flask_app = Flask(__name__)

@flask_app.route("/render_scene", methods=["POST"])
def render_scene_json():
    scene_json = request.get_json()

    ###############################################################################
    # Load the scene from JSON
    #
    json_parser = gsp_sc.renderer.json.JsonParser()
    canvas_loaded = json_parser.parse(scene_json)

    # print("Canvas loaded:", scene_json   )

    ###############################################################################
    # Render the loaded scene with matplotlib to visually verify it was loaded correctly
    #
    matplotlib_renderer = gsp_sc.renderer.matplotlib.MatplotlibRenderer()
    image_png_data = matplotlib_renderer.render(
        canvas_loaded, show_image=False
    )

    return send_file(
        io.BytesIO(image_png_data),
        mimetype="image/png",
        as_attachment=True,
        download_name="rendered_scene.png",
    )

#######################################################################################

if __name__ == "__main__":
    flask_app.run(threaded=False, debug=False)  # Enable debug mode if desired
