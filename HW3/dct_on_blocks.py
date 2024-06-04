import numpy as np
from scipy.fftpack import dct


def dct_on_blocks(image):
    # Ensure the image dimensions are divisible by 8
    height, width = image.shape[:2]
    if height % 8 != 0 or width % 8 != 0:
        raise ValueError("Image dimensions must be divisible by 8.")

    # Split the image into blocks of 8x8
    blocks = []
    for i in range(0, height, 8):
        for j in range(0, width, 8):
            block = image[i:i + 8, j:j + 8]
            blocks.append(block)

    # Apply DCT to each block and store the result
    dct_blocks = [dct(dct(block.T, norm='ortho').T, norm='ortho') for block in blocks]

    # Convert the list of DCT blocks into a 3D array
    dct_array = np.array(dct_blocks)
    dct_array = dct_array.reshape((height // 8, width // 8, 8, 8))

    return dct_array
