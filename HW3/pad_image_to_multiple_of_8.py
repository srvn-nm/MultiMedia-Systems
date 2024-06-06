import numpy as np


def pad_image_to_multiple_of_8(image):
    if len(image.shape) == 3:
        height, width, channels = image.shape
        new_height = (height + 7) // 8 * 8
        new_width = (width + 7) // 8 * 8
        padded_image = np.zeros((new_height, new_width, channels), dtype=image.dtype)
        padded_image[:height, :width, :] = image
    elif len(image.shape) == 2:
        height, width = image.shape
        new_height = (height + 7) // 8 * 8
        new_width = (width + 7) // 8 * 8
        padded_image = np.zeros((new_height, new_width), dtype=image.dtype)
        padded_image[:height, :width] = image
    else:
        raise ValueError("Unsupported image shape for padding")

    return padded_image
