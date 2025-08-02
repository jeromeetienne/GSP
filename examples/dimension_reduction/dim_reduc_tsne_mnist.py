import matplotlib.pyplot as plt

import libs.dim_reduct_data as dim_reduct_data
import libs.dim_reduc_fitting_tsne as dim_reduc_fitting_tsne
import libs.dim_reduc_display as dim_reduc_display

import os

# define __dirname__ to the directory of this script
__dirname__ = os.path.dirname(os.path.abspath(__file__))


###############################################################################
# Load MNIST data
#
mnist_x_train, mnist_y_train, mnist_x_test, mnist_y_test = dim_reduct_data.mnist_data_load()

###############################################################################
# Prepare data for t-SNE fitting
# - We will use the training data for t-SNE fitting
# - Flatten the images to 1D arrays for t-SNE
# - Each image is 28x28 pixels, so we will have 784 features per image

tsne_points_original, tsne_digits_original, tsne_colors = dim_reduct_data.mnist_data_prepare_fitting(mnist_x_train, mnist_y_train)

##########################################################################
# Fit t-SNE to the MNIST data
#

tsne_perplexity = 5.0  # You can adjust the perplexity parameter
tsne_points_fitted = dim_reduc_fitting_tsne.fit(tsne_points_original, perplexity=tsne_perplexity)

##########################################################################
# display the results
#

# Plot the t-SNE results
dim_reduc_display.display_matplotlib_scatter_plot(tsne_points_fitted, tsne_colors)

# add the label in the middle all the points
dim_reduc_display.display_matplotlib_point_labels(tsne_points_fitted, tsne_digits_original)

# Set the title and labels
plt.title(f"dimension reduction: t-SNE on MNIST Dataset (Perplexity={tsne_perplexity})")

###############################################################################
# Save the plot to a file
#
image_filename = os.path.join(__dirname__, '../output/dim_reduc_tsne_mnist.png')
plt.savefig(image_filename, dpi=300)

# Show the plot
plt.show()
