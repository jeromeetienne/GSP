import time
import numpy as np
from sklearn.manifold import TSNE


def fit(points_original: np.ndarray, perplexity: float = 30.0) -> np.ndarray:
    """
    Fit t-SNE to the original points.
    Args:
        points_original (np.ndarray): The original data points to fit.
        perplexity (float): The perplexity parameter for t-SNE.

    Returns:
        np.ndarray: The points transformed by t-SNE.
    """

    time_start = time.time()
    print("Fitting t-SNE...")

    # Create a t-SNE model
    tsne = TSNE(n_components=2, perplexity=perplexity)

    # Fit the model and transform the data
    tsne_points_fitted = tsne.fit_transform(points_original)

    time_elapsed = time.time() - time_start
    print(f"t-SNE fit_transform took {time_elapsed:.2f} seconds")
    return tsne_points_fitted
