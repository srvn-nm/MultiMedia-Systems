def inverse_quantize_dct_coefficients(quantized_dct_coefficients, quant_matrix):
    # Ensure the quantized DCT coefficients and quantization matrix have the correct shape
    if quantized_dct_coefficients.shape[2:] != quant_matrix.shape:
        raise ValueError("The shape of the quantization matrix must match the shape of the DCT blocks.")

    # Perform inverse quantization by element-wise multiplication
    inverse_quantized_coefficients = quantized_dct_coefficients * quant_matrix

    return inverse_quantized_coefficients
