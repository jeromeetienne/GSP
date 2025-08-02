import time
import numpy as np

load_time_start = time.time()
import umap
load_time_elapsed = time.time() - load_time_start
print(f"UMAP library loaded in {load_time_elapsed:.2f} seconds")


def fit(points_original: np.ndarray) -> np.ndarray:
    """
    Fit UMAP to the original points.
    Args:
        points_original (np.ndarray): The original data points to fit.
        
    Returns:
        np.ndarray: The points transformed by UMAP.
    """

    time_start = time.time()
    print("Fitting UMAP...")
    umap_fit = umap.UMAP()
    umap_points_fitted = umap_fit.fit_transform(points_original)
    time_elapsed = time.time() - time_start
    print(f"UMAP fit_transform took {time_elapsed:.2f} seconds")
    return umap_points_fitted
