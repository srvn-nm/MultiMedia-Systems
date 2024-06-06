import numpy as np

# Define standard quantization matrices
quant_matrix1 = np.array([
    [16, 11, 10, 16, 24, 40, 51, 61],
    [12, 12, 14, 19, 26, 58, 60, 55],
    [14, 13, 16, 24, 40, 57, 69, 56],
    [14, 17, 22, 29, 51, 87, 80, 62],
    [18, 22, 37, 56, 68, 109, 103, 77],
    [24, 35, 55, 64, 81, 104, 113, 92],
    [49, 64, 78, 87, 103, 121, 120, 101],
    [72, 92, 95, 98, 112, 100, 103, 99]
])
quant_matrix2 = quant_matrix1 * 1.5  # Example custom quantization matrix
quant_matrix3 = quant_matrix1 * 2.0  # Example custom quantization matrix


def quantize_dct_coefficients(dct_coefficients, quant_matrix=quant_matrix1):
    # Ensure the DCT coefficients and quantization matrix have the correct shape
    if dct_coefficients.shape[2:] != quant_matrix.shape:
        raise ValueError("The shape of the quantization matrix must match the shape of the DCT blocks.")

    # Perform quantization by element-wise division and rounding
    quantized_coefficients = np.round(dct_coefficients / quant_matrix)

    return quantized_coefficients
