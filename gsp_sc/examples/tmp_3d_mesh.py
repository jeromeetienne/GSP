from time import sleep

import matplotlib as mpl
import gsp_sc.src as gsp_sc
import numpy as np
import mpl3d.glm
import meshio

import os

__dirname__ = os.path.dirname(os.path.abspath(__file__))

###############################################################################
# Create a GSP scene
#
canvas = gsp_sc.core.Canvas(width=512, height=512, dpi=100)
viewport = gsp_sc.core.Viewport(
    origin_x=0,
    origin_y=0,
    width=canvas.width,
    height=canvas.height,
    background_color=gsp_sc.Constants.White,
)
canvas.add(viewport=viewport)

###############################################################################
# Add some random points
#

# Read the mesh .obj file
mesh_path = f"{__dirname__}/data/bunny.obj"
meshio_mesh = meshio.read(mesh_path)
mesh_vertices: np.ndarray = meshio_mesh.points
mesh_vertices = mpl3d.glm.fit_unit_cube(mesh_vertices)
mesh_faces: np.ndarray = meshio_mesh.cells[0].data

# mesh_vertices = np.array([[0,0,0]])
# mesh_vertices = np.?hstack([mesh_vertices, np.ones((mesh_vertices.shape[0], 1))])

# n_points = 10_000
# positions_np = np.random.uniform(-0.5, 0.5, (n_points, 3)).astype(np.float32)

transform_matrix = mpl3d.glm.translate(0, 0, 0) @ mpl3d.glm.xrotate(20) @ mpl3d.glm.yrotate(40) @ mpl3d.glm.zrotate(0) @ mpl3d.glm.scale(1)
positions_np:np.ndarray = mpl3d.glm.transform(mesh_vertices, transform_matrix)
positions_np = positions_np.astype(np.float32)

pixels = gsp_sc.visuals.Pixels(
    positions=positions_np, sizes=np.array([3]), colors=gsp_sc.Constants.Green
)
viewport.add(pixels)

###############################################################################
# Render the scene with matplotlib
#
# mpl3d_camera = mpl3d.camera.Camera("perspective")

renderer = gsp_sc.renderer.matplotlib.MatplotlibRendererDelta()
renderer.render(canvas)

