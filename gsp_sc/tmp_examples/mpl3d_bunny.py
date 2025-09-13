# -----------------------------------------------------------------------------
# Copyright (c) 2020 Nicolas P. Rougier. All rights reserved.
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------
# This example shows how to display a mesh
# -----------------------------------------------------------------------------
import mpl3d.camera
import mpl3d.glm
import mpl3d.mesh

import meshio
import mpl3d

import matplotlib.pyplot as plt

import os
__dirname__ = os.path.dirname(os.path.abspath(__file__))


mpl_figure = plt.figure(figsize=(4, 4))
mpl_axes = mpl_figure.add_axes([0, 0, 1, 1], xlim=[-1, +1], ylim=[-1, +1], aspect=1)
mpl_axes.axis("off")


# Set up the camera
def camera_update(transform) -> None:
    mesh.update(transform=transform)

mpl3d_camera = mpl3d.camera.Camera("perspective", scale=2)
mpl3d_camera.connect(mpl_axes, camera_update)

# Read the mesh .obj file
mesh_path = f"{__dirname__}/data/bunny.obj"
meshio_mesh = meshio.read(mesh_path)
mesh_vertices = meshio_mesh.points
mesh_vertices = mpl3d.glm.fit_unit_cube(mesh_vertices)
mesh_faces = meshio_mesh.cells[0].data
mesh = mpl3d.mesh.Mesh(
    ax=mpl_axes,
    transform=mpl3d_camera.transform,
    vertices=mesh_vertices,
    faces=mesh_faces,
    cmap=plt.get_cmap("magma"),
    edgecolors=(0, 0, 0, 0.25),
)

# Save an image scene
# image_path = f"{__dirname__}/output/bunny.png"
# plt.savefig(image_path, dpi=600)

# Show the scene in a window
plt.show()
