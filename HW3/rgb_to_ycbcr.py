import cv2
import numpy as np


def convert_rgb_to_ycbcr(image):
    # Convert color space from RGB to YCbCr using OpenCV
    ycbcr_image = cv2.cvtColor(image, cv2.COLOR_RGB2YCrCb)

    # Transpose the array to the format (channel, width, height)
    ndarray_ycbcr = np.transpose(ycbcr_image, (2, 0, 1))

    return ndarray_ycbcr
