from ...visuals.pixels import Pixels
from ...visuals.image import Image
from ...core.canvas import Canvas
from ...core.viewport import Viewport
import numpy as np

import json

class JsonRenderer:
    def __init__(self):
        pass

    def render(self, canvas: Canvas) -> str:

        scene_dict = {
            "canvas": {
                "width": canvas.width,
                "height": canvas.height,
                "dpi": canvas.dpi,
                "viewports": []
            }
        }

        for viewport in canvas.viewports:
            viewport_dict = {
                "origin_x": viewport.origin_x,
                "origin_y": viewport.origin_y,
                "width": viewport.width,
                "height": viewport.height,
                "background_color": viewport.background_color,
                "visuals": []
            }


            for visual in viewport.visuals:
                if isinstance(visual, Pixels):
                    visual_dict = {
                        "type": "Pixels",
                        "positions": visual.positions.tolist(),
                        "sizes": visual.sizes.tolist(),
                        "colors": visual.colors
                    }
                elif isinstance(visual, Image):
                    visual_dict = {
                        "type": "Image",
                        "bounds": visual.bounds,
                        "image_data_shape": visual.image_data.shape,
                        "image_data": visual.image_data.tolist()
                    }
                else:
                    raise NotImplementedError(
                        f"Rendering for visual type {type(visual)} is not implemented."
                    )

                viewport_dict["visuals"].append(visual_dict)

            scene_dict["canvas"]["viewports"].append(viewport_dict)

        scene_json = json.dumps(scene_dict, indent=4)

        return scene_json
