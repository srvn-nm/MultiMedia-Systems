# Arithmetic coding functions
import numpy as np

from ArithmeticEncoder import ArithmeticEncoder
from Model import Model


def arithmetic_encode(dct_coefficients):
    flat_coefficients = dct_coefficients.flatten()
    unique_vals, counts = np.unique(flat_coefficients, return_counts=True)
    probabilities = counts / counts.sum()

    model = Model(unique_vals, probabilities)
    encoder = ArithmeticEncoder(model)

    for symbol in flat_coefficients:
        encoder.encode(symbol)

    encoded_image = encoder.finish()
    return encoded_image, model
