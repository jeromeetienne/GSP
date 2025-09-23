import gsp
from gsp import core, visual
from gsp_matplotlib import glm
import numpy as np

from common.launcher import parse_args
from gsp_matplotlib import glm

# Parse command line arguments
core, visual, render = parse_args()

# Build a scene
canvas = core.Canvas(512, 512, 100.0)
viewport = core.Viewport(canvas, 0, 0, 512, 512, [1,1,1,1])
n = 200_000
P = glm.to_vec3(np.random.uniform(-1, +1, (n,2)), dtype=np.float32)
pixels = visual.Pixels(positions=P, colors=[0,0,0,1])
pixels.render(viewport)

# Save a command file
import os
__dirname__ = os.path.dirname(os.path.abspath(__file__))

commands_filename = f"{__dirname__}/output/test-command-file-cycle.command.json"
gsp.save(filename=commands_filename)

# breakpoint()

#########
# Now reset everything and reload from command file, then run the queue
# 

gsp.use("matplotlib")

##################################################################################

# reset objects
gsp.Object.objects = {}

# load commands from file
command_queue = gsp.io.json.load(commands_filename)

command_queue.run(globals(), locals())

#####################################
# Finally display the result via matplotlib

import matplotlib.pyplot as plt
plt.show(block=True)