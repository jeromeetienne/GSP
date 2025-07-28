import libs.point_cloud_lib as point_cloud_lib
import libs.point_cloud_bench as point_cloud_bench
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
# Perform 3d transform
#

# Compute the model-view-projection matrix
matrix_model = xrotate(20) @ yrotate(0)
matrix_view = translate(0, 0, -3.5)
matrix_projection = perspective(25, 1, 0.1, 100)
matrix_model_view_projection = matrix_projection @ matrix_view @ matrix_model

# convert to homogeneous coordinates and apply the MVP matrix
point_positions = (
    np.c_[point_positions, np.ones(len(point_positions))]
    @ matrix_model_view_projection.T
)

# Normalize point_positions for homogeneous coordinates
point_positions /= point_positions[:, 3].reshape(-1, 1)

###############################################################################
# Compose figure
#

# figure = plt.figure(figsize=(3, 3))
# # axes = figure.add_subplot(projection='3d')
# axe = figure.add_subplot()
# # hide axis

# axe.scatter(point_positions[:, 0], point_positions[:, 1], color=[1,0,0,1], s=1, rasterized=True)
# # ax.scatter(point_positions[:, 0], point_positions[:, 1], color=point_colors, s=1, rasterized=True)
# # axes.scatter(point_positions[:, 0], point_positions[:, 1], marker='.', color=point_colors)

# # axes.set_pro
# # axes.scatter(
# #     point_positions[:, 0],
# #     point_positions[:, 1],
# #     point_positions[:, 2],
# #     color=[1,0,0,1],
# #     # color=point_colors,
# #     s=1,
# #     rasterized=True,
# # )

# # disable the grid
# axe.axis("off")

###############################################################################
# Rendering 
#

measure_rendering_time = True  # Set to True to measure rendering time

if measure_rendering_time is False:
    # plt.scatter(point_positions[:, 0], point_positions[:, 1], color=[1,0,0,1], s=1, rasterized=True)
    plt.scatter(point_positions[:, 0], point_positions[:, 1], color=point_colors, s=1, rasterized=True)

    plt.show(block=True)
    exit()


figsize = (3, 3)  # Size of the figure in inches
max_bench_delay_seconds = 10.0  # Maximum time to wait for the benchmark in seconds

##########################################################################
# Benchmark rendering performance with monochrome points
#

if True:
    print("Rendering the point cloud with Matplotlib... monochrome")
    figure = plt.figure(figsize=figsize)
    axe = figure.add_subplot()
    axe.axis("off")  # Hide the axis
    axe.scatter(point_positions[:, 0], point_positions[:, 1], color=[1,0,0,1], s=1, rasterized=True)
    rendering_time = point_cloud_bench.display_benchmark_pure_matplotlib(figure=figure, log_enabled=True, max_bench_delay_seconds=max_bench_delay_seconds)
    print(f"Average rendering time: {rendering_time:.6f} seconds per rendering.")

    # Close the figure
    plt.close(figure)

############################################################################
# Render the point cloud with colors
#
if True:
    print("Rendering the point cloud with Matplotlib... colored")
    figure = plt.figure(figsize=figsize)
    axe = figure.add_subplot()
    axe.axis("off")  # Hide the axis
    axe.scatter(point_positions[:, 0], point_positions[:, 1], color=point_colors, s=1, rasterized=True)
    rendering_time = point_cloud_bench.display_benchmark_pure_matplotlib(figure=figure, log_enabled=True, max_bench_delay_seconds=max_bench_delay_seconds)
    print(f"Average rendering time: {rendering_time:.6f} seconds per rendering.")

    # Close the figure
    plt.close(figure)


###############################################################################
# benchmark rendering performance with monochrome markers
#

if True:
    print("Rendering the point cloud with Matplotlib... monochrome markers")
    figure = plt.figure(figsize=figsize)
    axe = figure.add_subplot()
    axe.axis("off")  # Hide the axis
    axe.scatter(point_positions[:, 0], point_positions[:, 1], marker='o', color=[1,0,0,1], s=1, rasterized=True)
    rendering_time = point_cloud_bench.display_benchmark_pure_matplotlib(figure=figure, log_enabled=True, max_bench_delay_seconds=max_bench_delay_seconds)
    print(f"Average rendering time: {rendering_time:.6f} seconds per rendering.")

    # Close the figure
    plt.close(figure)

###############################################################################
# benchmark rendering performance with colored markers
#
if True:
    print("Rendering the point cloud with Matplotlib... colored markers")
    figure = plt.figure(figsize=figsize)
    axe = figure.add_subplot()
    axe.axis("off")  # Hide the axis
    axe.scatter(point_positions[:, 0], point_positions[:, 1], marker='.', color=point_colors, s=1, rasterized=True)
    rendering_time = point_cloud_bench.display_benchmark_pure_matplotlib(figure=figure, log_enabled=True, max_bench_delay_seconds=max_bench_delay_seconds)
    print(f"Average rendering time: {rendering_time:.6f} seconds per rendering.")

    # Close the figure
    plt.close(figure)