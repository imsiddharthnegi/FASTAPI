"""
Vectorization utilities for images.
"""

import cv2
import numpy as np
from typing import List

def compute_histogram(image_path: str) -> np.ndarray:
    """
    Compute a BGR color histogram feature vector for an image.
    Returns a 768-dimensional vector (256 bins per channel).
    """
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError(f"Could not open image {image_path}")
    chans = cv2.split(img)
    features: List[float] = []
    for chan in chans:
        hist = cv2.calcHist([chan], [0], None, [256], [0, 256]).flatten()
        hist = hist / hist.sum() if hist.sum() > 0 else hist  # Normalize, avoid zero division
        features.extend(hist)
    return np.array(features, dtype=np.float32)