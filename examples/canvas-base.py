# Package: Graphic Server Protocol / Matplotlib
# Authors: Nicolas P .Rougier <nicolas.rougier@gmail.com>
# License: BSD 3 clause
"""
Canvas (base)
=============

This example shows how to create a canvas with a size specified using
some units (centimeter) and how t enter the event loop (matplotlib).
"""
# Experiment to handle intellisense in VSCode
import matplotlib.pyplot as plt
import numpy as np

from gsp import core, transform, visual, glm
import gsp
gsp.use("matplotlib")

cm = transform.Centimeter()
canvas = core.Canvas(10*cm, 10*cm, 100.0)

plt.savefig("./output/canvas-base.png")
plt.show()
