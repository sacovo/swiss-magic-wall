"""
Util functions for calculating projections
"""
import tempfile
from django.core.files import File

import numpy as np


def calculate_projection(old_data: np.ndarray) -> np.ndarray:
    """
    Calculates the projection used to calculate the prediction
    """
    col_means = np.nanmean(old_data, axis=0)
    nan_places = np.where(np.isnan(old_data))

    old_data[nan_places] = np.take(col_means, nan_places[1])

    u, s, _ = np.linalg.svd(old_data, full_matrices=False)
    s = np.diag(s)
    return np.dot(u, s)


def save_projection_to_file(projection: np.ndarray, field, pk: int, key: str):
    """Save the projection to the database"""
    with tempfile.TemporaryFile() as output_file:
        np.save(output_file, projection)
        output_file.seek(0)
        field.save(f"{pk}-{key}.projection.npy", File(output_file))


def prediction(projection, values, indexes):
    """
    Predicts the result for the missing communities
    """
    observed_projection = projection[indexes]
    tmp = np.linalg.inv((np.dot(observed_projection.T, observed_projection) +
                         0.01 * np.identity(projection.shape[1])))
    tmp2 = np.dot(tmp, observed_projection.T)
    w = np.dot(tmp2, values[indexes])

    return np.dot(projection[~indexes], w)
