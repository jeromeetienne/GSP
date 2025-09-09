# Package: Graphic Server Protocol
# Authors: Nicolas P .Rougier <nicolas.rougier@gmail.com>
# License: BSD 3 clause
"""
Pixels visual (2D)
==================

This example shows the Pixels visual where pixels are spread randomly
inside a square that can be zoomed using the mouse and an orthographic
camera.
"""
import gsp

import matplotlib.pyplot as plt
import numpy as np
import os



canvas = gsp.core.Canvas(512, 512, 100.0)
viewport = gsp.core.Viewport(canvas, 0, 0, 512, 512, [1,1,1,1])

display_enabled = False

if display_enabled:
    n_points = 250
    positions_np = np.random.uniform(-1, +1, (n_points,3))
    positions_vec3 = gsp.glm.to_vec3(positions_np)

    pixels = gsp.matplotlib.visual.Pixels(positions_vec3, colors=[0,0,0,1])
    pixels.render(viewport)

    # save a screenshot of the rendered canvas
    image_filename = f"{os.path.dirname(os.path.abspath(__file__))}/output/text_io_pixels.png"

    plt.savefig(image_filename)
    plt.show()

    # commands_filename = f"{os.path.dirname(os.path.abspath(__file__))}/output/text_io_pixels_gsp_commands.json"
    # gsp.save(commands_filename)
else:
    n_points = 20_000
    positions_np = np.random.uniform(-1, +1, (n_points,3)).astype(np.float32)
    # positions_np = np.ones((n_points,3), dtype=np.float32)
    positions_vec3 = positions_np

    # positions_vec3 = glm.to_vec3(positions_np)
    # convert positions_np to a 3d numpy array
    # positions_vec3 = np.zeros((n_points,3), dtype=np.float32)
    # positions_vec3[:,:2] = positions_np
    # positions_vec3[:,2] = 0.0

    # buffer_count = positions_vec3.shape[0] * positions_vec3.shape[1]
    buffer_count = positions_vec3.size
    buffer_dtype = positions_vec3.dtype
    buffer_data = positions_vec3.data
    # breakpoint()

    # create an np.ndarray from buffer_data
    # buffer_data_np = np.frombuffer(buffer_data, dtype=buffer_dtype, count=buffer_count)
    # buffer_data_np = buffer_data_np.reshape((n_points, 3))

    # import gsp.matplotlib.core as gsp_core

    position_buffer = gsp.core.Buffer(buffer_count, buffer_dtype, buffer_data)

    # position_vec3_bis = glm.to_vec3(position_buffer)
    pixels = gsp.visual.Pixels(position_buffer, colors=[0,0,0,1])
    pixels.render(viewport)

    commands_filename = f"{os.path.dirname(os.path.abspath(__file__))}/output/text_io_pixels.commands.json"
    gsp.save(commands_filename)

###################################################
# Re-load commands and re-execute them
###################################################

# from gsp import Object
# from gsp.log import log

import logging
gsp.log.setLevel(logging.INFO)

gsp.Object.objects = {}
commands_filename = f"{os.path.dirname(os.path.abspath(__file__))}/output/text_io_pixels.commands.json"
command_queue = gsp.io.json.load(commands_filename)
for command in command_queue:
    gsp.log.info("%s" % command)

# KEY: REQUIRED FOR THE GLOBALS
gsp.use('matplotlib')

# TODO send matplotlib as namespace in command_queue.run
command_queue.run(globals(), locals())
print(Object.objects[1])
print()

plt.show(block=True)
