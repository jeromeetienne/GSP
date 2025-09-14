from ...visuals.pixels import Pixels
from ...visuals.image import Image
from ...core.canvas import Canvas
from ...core.viewport import Viewport
import numpy as np

import json


class JsonParser:
    def __init__(self) -> None:
        pass

    def parse(self, scene_json: str) -> Canvas:
        scene_dict = json.loads(scene_json)

        canvas_info = scene_dict["canvas"]
        canvas = Canvas(canvas_info["width"], canvas_info["height"], canvas_info["dpi"])

        for viewport_info in canvas_info["viewports"]:
            viewport = Viewport(
                origin_x=viewport_info["origin_x"],
                origin_y=viewport_info["origin_y"],
                width=viewport_info["width"],
                height=viewport_info["height"],
                background_color=viewport_info["background_color"],
            )
            canvas.add(viewport)

            for visual_info in viewport_info["visuals"]:
                if visual_info["type"] == "Pixels":
                    visual = Pixels(
                        positions=np.array(visual_info["positions"]),
                        sizes=np.array(visual_info["sizes"]),
                        colors=visual_info["colors"],
                    )
                elif visual_info["type"] == "Image":
                    image_data_shape = tuple(visual_info["image_data_shape"])
                    image_data = np.array(visual_info["image_data"]).reshape(
                        image_data_shape
                    )
                    visual = Image(image_extent=visual_info["bounds"], image_data=image_data)
                else:
                    raise NotImplementedError(
                        f"Parsing for visual type {visual_info['type']} is not implemented."
                    )

                viewport.add(visual)

        return canvas
