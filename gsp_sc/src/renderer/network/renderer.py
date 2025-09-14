from ...core.canvas import Canvas
from ...core.camera import Camera
import numpy as np

from ..json.renderer import JsonRenderer

import json
import requests


class NetworkRenderer:
    __slots__ = ("server_url",)
    def __init__(self, server_url: str) -> None:
        self.server_url = server_url

    def render(self, canvas: Canvas, camera: Camera) -> bytes:
        # Convert the canvas to JSON
        renderer_json = JsonRenderer()
        scene_json = renderer_json.render(canvas, camera)

        # Send the POST request with JSON data
        call_url = f"{self.server_url}/render_scene"
        headers = {"Content-Type": "application/json"}
        response = requests.post(call_url, data=json.dumps(scene_json), headers=headers)

        # Check the response status
        if response.status_code != 200:
            raise Exception(f"Request failed with status code {response.status_code}")

        # return png data as bytes
        image_png_data = response.content
        return image_png_data
