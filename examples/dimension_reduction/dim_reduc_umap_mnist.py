import matplotlib.pyplot as plt

import common.dim_reduct_data as dim_reduct_data
import common.dim_reduc_fitting_umap as dim_reduc_fitting_umap

import os
# define __dirname__ to the directory of this script
__dirname__ = os.path.dirname(os.path.abspath(__file__))

###############################################################################
# Load MNIST data
#
mnist_x_train, mnist_y_train, mnist_x_test, mnist_y_test = dim_reduct_data.mnist_data_load()

###############################################################################
# Prepare data for UMAP fitting
# - We will use the training data for UMAP fitting
# - Flatten the images to 1D arrays for UMAP
# - Each image is 28x28 pixels, so we will have 784 features per image

umap_points_original, umap_digits_original, umap_colors = dim_reduct_data.mnist_data_prepare_fitting(mnist_x_train, mnist_y_train)

##########################################################################
# Fit UMAP to the MNIST data
#

umap_points_fitted = dim_reduc_fitting_umap.fit(umap_points_original)

##########################################################################
# display the results
#

display_type='plain_matplotlib'
# display_type='gsp_matplotlib'

image_filename = os.path.join(__dirname__, '../output/dim_reduc_umap_mnist.png')

if display_type=='gsp_matplotlib':
    import common.dim_reduc_display_gsp as dim_reduc_display_gsp

    # display 
    dim_reduc_display_gsp.display_gsp_scatter_plot(points_fitted=umap_points_fitted, points_colors=umap_colors, image_filename=image_filename)
else:
    import common.dim_reduc_display_matplotlib as dim_reduc_display_matplotlib
    # Plot the UMAP results
    dim_reduc_display_matplotlib.display_matplotlib_scatter_plot(umap_points_fitted, umap_colors)

    # add the label in the middle all the points
    dim_reduc_display_matplotlib.display_matplotlib_point_labels(umap_points_fitted, umap_digits_original)

    # Set the title and labels
    plt.title("dimension reduction: UMAP on MNIST Dataset")

    ###############################################################################
    # Save the plot to a file
    # 
    plt.savefig(image_filename, dpi=300)

    # Show the plot
    plt.show()
