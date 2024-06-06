import numpy as np

from ArithmeticDecoder import ArithmeticDecoder


def arithmetic_decode(encoded_image, model, shape):
    decoder = ArithmeticDecoder(encoded_image, model)
    decoded_coefficients = []

    for _ in range(np.prod(shape)):
        decoded_coefficients.append(decoder.decode())

    decoded_array = np.array(decoded_coefficients).reshape(shape)
    return decoded_array
