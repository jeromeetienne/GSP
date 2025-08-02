import requests
import numpy as np
import matplotlib.pyplot as plt
import os

# TODO use download.py from datoviz library


# define __dirname__ to the directory of this script
__dirname__ = os.path.dirname(os.path.abspath(__file__))


def mnist_data_load() -> tuple:
    """
    Load MNIST data from a remote source and return training and test sets.

    Returns:
        tuple: (mnist_x_train, mnist_y_train, mnist_x_test, mnist_y_test)
    """
    # url from https://www.kaggle.com/datasets/vikramtiwari/mnist-numpy
    mnist_url = "https://storage.googleapis.com/tensorflow/tf-keras-datasets/mnist.npz"
    request = requests.get(mnist_url, stream=True, timeout=30)

    file_path = os.path.join(__dirname__, "../data/mnist.npz")

    with open(file_path, "wb") as fileWriter:
        fileWriter.write(request.content)

    # print(f"Request status code: {request.status_code}")

    mnist_data = np.load(file_path)

    # print(f"mnist_data.files: {mnist_data.files}")

    mnist_x_train = mnist_data["x_train"]
    mnist_y_train = mnist_data["y_train"]
    mnist_x_test = mnist_data["x_test"]
    mnist_y_test = mnist_data["y_test"]

    return mnist_x_train, mnist_y_train, mnist_x_test, mnist_y_test


def mnist_data_prepare_fitting(
    mnist_x_train: np.ndarray, mnist_y_train: np.ndarray,
    max_element_count: int = 10000
) -> tuple:
    """
    Prepare MNIST data for fitting (umap, etc...).

    Args:
        mnist_x_train (np.ndarray): Training images.
        mnist_y_train (np.ndarray): Training labels.

    Returns:
        tuple: (umap_points_original, umap_digits_original, umap_colors)
    """
    umap_element_count = min(len(mnist_x_train), max_element_count)
    umap_points_original = np.empty((umap_element_count, mnist_x_train[0].flatten().shape[0]))
    umap_digits_original = np.empty((umap_element_count, 1))
    umap_colors = np.empty((umap_element_count, 4))
    umap_cmap = plt.get_cmap('hsv')

    for i in range(umap_element_count):
        umap_points_original[i] = mnist_x_train[i].flatten()
        umap_digits_original[i] = mnist_y_train[i].flatten()
        umap_colors[i] = umap_cmap(mnist_y_train[i] / 10)  # Normalize label to [0, 1] for color mapping

    return umap_points_original, umap_digits_original, umap_colors