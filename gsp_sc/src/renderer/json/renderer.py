from ...visuals.pixels import Pixels
from ...visuals.image import Image
from ...core.canvas import Canvas
from ...core.viewport import Viewport
import numpy as np

import json


class JsonRenderer:
    def __init__(self) -> None:
        pass

    def render(self, canvas: Canvas) -> str:

        scene_dict = {
            "canvas": {
                "uuid": canvas.uuid,
                "width": canvas.width,
                "height": canvas.height,
                "dpi": canvas.dpi,
                "viewports": [],
            }
        }

        for viewport in canvas.viewports:
            viewport_dict = {
                "uuid": viewport.uuid,
                "origin_x": viewport.origin_x,
                "origin_y": viewport.origin_y,
                "width": viewport.width,
                "height": viewport.height,
                "background_color": viewport.background_color,
                "visuals": [],
            }

            for visual in viewport.visuals:
                if isinstance(visual, Pixels):
                    pixels: Pixels = visual
                    visual_dict = {
                        "type": "Pixels",
                        "uuid": pixels.uuid,
                        "positions": pixels.positions.tolist(),
                        "sizes": pixels.sizes.tolist(),
                        "colors": pixels.colors,
                    }
                elif isinstance(visual, Image):
                    image: Image = visual
                    visual_dict = {
                        "type": "Image",
                        "uuid": image.uuid,
                        "position": image.position.tolist(),
                        "bounds": image.image_extent,
                        "image_data_shape": image.image_data.shape,
                        "image_data": image.image_data.tolist(),
                    }
                else:
                    raise NotImplementedError(
                        f"Rendering for visual type {type(visual)} is not implemented."
                    )

                viewport_dict["visuals"].append(visual_dict)

            scene_dict["canvas"]["viewports"].append(viewport_dict)

        scene_json = json.dumps(scene_dict, indent=4)

        return scene_json
