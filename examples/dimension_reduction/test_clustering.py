import numpy as np
from sklearn.cluster import DBSCAN

X = np.array([[1, 2], [2, 2], [2, 3], [8, 7], [8, 8], [25, 80]])

db = DBSCAN(eps=3, min_samples=2)
labels = db.fit_predict(X)

pass

# db = DBSCAN(eps=3, min_samples=2)
# db.fit(X)
# labels = db.labels_

