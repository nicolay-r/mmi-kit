import numpy as np


class PixelarrayService:

    @staticmethod
    def scale(pixel_array, factor=255.0):
        min_val = np.min(pixel_array)
        max_val = np.max(pixel_array)
        return (((pixel_array - min_val) / (max_val - min_val)) * factor) if max_val > min_val else pixel_array
