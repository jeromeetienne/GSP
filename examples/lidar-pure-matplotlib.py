import libs.point_cloud_lib as point_cloud_lib
import libs.download as download
from libs.projection_matrix import frustum, perspective
from libs.transformation_matrix import translate, xrotate, yrotate

# import matplotlib
# matplotlib.use('Agg')

# Experiment to handle intellisense in VSCode
import matplotlib.pyplot as plt
import numpy as np

# display matplotlib backend
print(f"Matplotlib backend: {plt.get_backend()}")

import time
import os
# define __dirname__ to the directory of this script
__dirname__ = os.path.dirname(os.path.abspath(__file__))

import matplotlib.style as mplstyle
# mplstyle.use('fast')

###############################################################
# Load the LIDAR data
#

point_positions, point_colors = point_cloud_lib.load_npz_point_cloud(
    download.download_data("misc/lidar.npz")
)

print(f"Loaded LIDAR data with {len(point_positions)} points.")

point_cloud_lib.print_geometry_info(point_positions)

###############################################################################
# Crop geometry
#
point_positions, point_colors = point_cloud_lib.geometry_crop(
    point_positions=point_positions,
    point_colors=point_colors,
    x_min=-0.1,
    x_max=0.1,
    z_min=-0.1,
    z_max=0.1,
)

print(f"Loaded LIDAR data with {len(point_positions)} points.")

###############################################################################
# Downsample the point cloud
#

point_positions, point_colors = point_cloud_lib.downsample(
    point_positions=point_positions,
    point_colors=point_colors,
    # wished_point_count=5_000_000
#     wished_point_count=2_000_000,
    # wished_point_count=500_000,
    wished_point_count=200_000,
    # wished_point_count=50_000,
    # wished_point_count=10_000,
)

print(f"Downsampling - Keeping {len(point_positions)} points after downsampling.")


##################################################################################

# Compute the model-view-projection matrix
matrix_model = xrotate(20) @ yrotate(0)
matrix_view  = translate(0,0,-3.5)
matrix_projection  = perspective(25, 1, 0.1, 100)
matrix_model_view_projection   = matrix_projection  @ matrix_view  @ matrix_model

# convert to homogeneous coordinates and apply the MVP matrix
point_positions = np.c_[point_positions, np.ones(len(point_positions))] @ matrix_model_view_projection.T
# Normalize point_positions for homogeneous coordinates
point_positions /= point_positions[:,3].reshape(-1,1)

###############################################################################
# Display the point cloud using Matplotlib scatter plot
#

figure = plt.figure(figsize=(10,10))
axe = figure.add_axes([0, 0, 1, 1], xlim=[-1, +1], ylim=[-1, +1], aspect=1, frameon=False)
start_time = time.time()
# axe.scatter(point_positions[:, 0], point_positions[:, 1], c=point_colors, s=3, rasterized=True)
axe.scatter(point_positions[:, 0], point_positions[:, 1], color=[1,0,0,1], s=1, rasterized=False)

# plt.savefig(f"{__dirname__}/output/lidar_point_cloud.png", dpi=300, bbox_inches='tight', pad_inches=0.1)
plt.savefig(f"{__dirname__}/output/lidar_point_cloud_pure_matplotlib.png", dpi=50)
# plt.show(block=True)

elapsed_time = time.time() - start_time
print(f"Rendering took {elapsed_time:.2f} seconds or {1/elapsed_time:.2f} FPS.")
# plt.savefig(f"{__dirname__}/output/lidar_point_cloud_pure_matplotlib.png", dpi=100)
# plt.show()
exit()

################################################################################
# Measure the time taken for visualization
#
start_time = time.time()

# remove the axis
plt.axis("off")
plt.scatter(point_positions[:, 0], point_positions[:, 1], c=point_colors, s=1, rasterized=True)
# plt.scatter(point_positions[:, 0], point_positions[:, 1], color=[1,1,1,1], s=1, rasterized=True)
# plt.plot(
#     point_positions[:, 0], point_positions[:, 1], marker='.', linestyle='None',
#     markersize=1, color=point_colors, rasterized=True
# #    marker='.', linestyle='None', color=point_colors, markersize=1, rasterized=True
# )


# measure_rendering_time = True  # Set to True to measure rendering time
measure_rendering_time = False  # Set to True to measure rendering time

if measure_rendering_time is False:
    plt.show(block=True)
else:
    plt.show(block=False)

elapsed_time = time.time() - start_time
if measure_rendering_time:
    print(f"Rendering took {elapsed_time:.2f} seconds or {1/elapsed_time:.2f} FPS.")
