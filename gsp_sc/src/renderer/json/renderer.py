# stdlib imports
import typing
import json

# pip imports
import numpy as np

# local imports
from ...core.canvas import Canvas
from ...core.camera import Camera
from ...visuals.pixels import Pixels
from ...visuals.image import Image
from ...visuals.mesh import Mesh
from ...transform import TransformOrNdarray


class JsonRenderer:
    def __init__(self) -> None:
        pass

    def render(self, canvas: Canvas, camera: Camera) -> str:

        scene_dict = {
            "camera": {
                "uuid": camera.uuid,
                "type": camera.camera_type,
            },
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
                        "positions": TransformOrNdarray.to_json(pixels.positions),
                        "sizes": TransformOrNdarray.to_json(pixels.sizes),
                        "colors": TransformOrNdarray.to_json(pixels.colors),
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
                elif isinstance(visual, Mesh):
                    mesh = visual
                    visual_dict = {
                        "type": "Mesh",
                        "uuid": mesh.uuid,
                        "vertices": mesh.vertices.tolist(),
                        "cmap": None if mesh.cmap is None else mesh.cmap.name,
                        "faces": mesh.faces.tolist(),
                        "facecolors": mesh.facecolors.tolist(),
                        "edgecolors": mesh.edgecolors.tolist(),
                        "linewidths": mesh.linewidths,
                        "mode": mesh.mode,
                    }
                else:
                    raise NotImplementedError(f"Rendering for visual type {type(visual)} is not implemented.")

                viewport_dict["visuals"].append(visual_dict)

            scene_dict["canvas"]["viewports"].append(viewport_dict)

        scene_json = json.dumps(scene_dict, indent=4)

        return scene_json
