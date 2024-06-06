import numpy as np
from scipy.fftpack import dct, idct


def dct_on_blocks(image):
    if len(image.shape) == 3:
        height, width, channels = image.shape
        dct_array = np.zeros_like(image, dtype=float)

        for channel in range(channels):
            for i in range(0, height, 8):
                for j in range(0, width, 8):
                    block = image[i:i + 8, j:j + 8, channel]
                    dct_array[i:i + 8, j:j + 8, channel] = dct(dct(block, axis=0, norm='ortho'), axis=1, norm='ortho')

        return dct_array
    elif len(image.shape) == 2:
        height, width = image.shape
        dct_array = np.zeros_like(image, dtype=float)

        for i in range(0, height, 8):
            for j in range(0, width, 8):
                block = image[i:i + 8, j:j + 8]
                dct_array[i:i + 8, j:j + 8] = dct(dct(block, axis=0, norm='ortho'), axis=1, norm='ortho')

        return dct_array
    else:
        raise ValueError("Unsupported image shape for DCT")


def inverse_dct_on_blocks(dct_coefficients):
    if len(dct_coefficients.shape) == 3:
        height, width, channels = dct_coefficients.shape
        image = np.zeros_like(dct_coefficients, dtype=float)

        for channel in range(channels):
            for i in range(0, height, 8):
                for j in range(0, width, 8):
                    block = dct_coefficients[i:i + 8, j:j + 8, channel]
                    image[i:i + 8, j:j + 8, channel] = idct(idct(block, axis=0, norm='ortho'), axis=1, norm='ortho')

        return image
    elif len(dct_coefficients.shape) == 2:
        height, width = dct_coefficients.shape
        image = np.zeros_like(dct_coefficients, dtype=float)

        for i in range(0, height, 8):
            for j in range(0, width, 8):
                block = dct_coefficients[i:i + 8, j:j + 8]
                image[i:i + 8, j:j + 8] = idct(idct(block, axis=0, norm='ortho'), axis=1, norm='ortho')

        return image
    else:
        raise ValueError("Unsupported DCT coefficients shape")
