import numpy as np


def convert_ycbcr_to_rgb(ycbcr_image):
    # Get the dimensions of the YCbCr image
    height, width, _ = ycbcr_image.shape

    # Create an array to hold the RGB image
    rgb_image = np.zeros((height, width, 3), dtype=np.uint8)

    # Extract the Y, Cb, and Cr channels
    Y = ycbcr_image[:, :, 0]
    Cb = ycbcr_image[:, :, 1]
    Cr = ycbcr_image[:, :, 2]

    # Perform the inverse color space transformation
    R = Y + 1.402 * (Cr - 128)
    G = Y - 0.344136 * (Cb - 128) - 0.714136 * (Cr - 128)
    B = Y + 1.772 * (Cb - 128)

    # Clip the values to the valid range [0, 255] and assign to the RGB image
    rgb_image[:, :, 0] = np.clip(R, 0, 255)
    rgb_image[:, :, 1] = np.clip(G, 0, 255)
    rgb_image[:, :, 2] = np.clip(B, 0, 255)

    return rgb_image
