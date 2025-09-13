from flask import Flask, jsonify, request, send_file
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
    import os
    __dirname__ = os.path.dirname(os.path.abspath(__file__))
    rendered_loaded_image_path = f"{__dirname__}/output/rendered_loaded_image.png"
    matplotlib_renderer = gsp_sc.renderer.matplotlib.MatplotlibRenderer()
    matplotlib_renderer.render(
        canvas_loaded, show_image=False, image_filename=rendered_loaded_image_path
    )

    return send_file(rendered_loaded_image_path, mimetype='image/png')

#######################################################################################

if __name__ == "__main__":
    flask_app.run(threaded=False, debug=True)  # Enable debug mode if desired
