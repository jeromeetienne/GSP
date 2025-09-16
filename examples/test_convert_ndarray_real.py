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
from gsp import core, visual, glm
import numpy as np

canvas = core.Canvas(512, 512, 100.0)
viewport = core.Viewport(canvas, 0, 0, 512, 512, [1,1,1,1])
n = 20
P = glm.to_vec3(np.random.uniform(-1, +1, (n,2)), dtype=np.float32)
# P = glm.to_vec3([[1,2],[3,4],], dtype=np.float32)


# P = glm.to_vec3(np.random.uniform(-1, +1, (n,2)), dtype=np.float32)

positions_np = np.random.uniform(-1, +1, (n,2))
buffer_count = positions_np.size
buffer_dtype = positions_np.dtype
buffer_data = positions_np.data
position_buffer = core.Buffer(buffer_count, buffer_dtype, buffer_data)

pixels = visual.Pixels(positions=positions_np, colors=[0,0,0,1])
pixels.render(viewport)

# Save a command file
import os
__dirname__ = os.path.dirname(os.path.abspath(__file__))
commands_filename = f"{__dirname__}/output/{os.path.basename(__file__).replace('.py', '')}.command.json"
gsp.save(filename=commands_filename)

# exit the script
import sys
sys.exit(0)

#######################################################
# reset gsp, reload the command.json and render it with matpotlib

# reset objects - TODO make it cleaner - call a function e.g. .clear() ?
gsp.Object.objects = {}

# load commands from file
command_queue = gsp.io.json.load(commands_filename)

for command in command_queue:
        gsp.log.info("%s" % command)

# KEY: REQUIRED FOR THE GLOBALS - Super dirty!!!
gsp.use("matplotlib")

# TODO send matplotlib as namespace in command_queue.run
command_queue.run(globals(), locals())
# print(f"object: {gsp.Object.objects[1]}")

import matplotlib.pyplot as plt
plt.show(block=True)