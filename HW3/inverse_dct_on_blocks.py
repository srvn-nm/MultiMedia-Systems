import numpy as np
import cv2


def inverse_dct_on_blocks(dequantized_dct_coefficients):
    # Get the shape of the DCT coefficient array
    channels, height_blocks, width_blocks, block_size, _ = dequantized_dct_coefficients.shape

    # Create an array to hold the reconstructed image
    reconstructed_image = np.zeros((channels, height_blocks * block_size, width_blocks * block_size))

    # Perform inverse DCT on each block
    for c in range(channels):
        for i in range(height_blocks):
            for j in range(width_blocks):
                # Extract the block
                block = dequantized_dct_coefficients[c, i, j]
                # Perform inverse DCT
                idct_block = cv2.idct(block)
                # Place the reconstructed block in the reconstructed image array
                reconstructed_image[c, i * block_size:(i + 1) * block_size,
                j * block_size:(j + 1) * block_size] = idct_block

    return reconstructed_image
