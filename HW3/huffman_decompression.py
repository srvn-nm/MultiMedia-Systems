from HuffmanNode import huffman_decode
from inverse_dct_on_blocks import inverse_dct_on_blocks
from inverse_quantize_dct_coefficients import inverse_quantize_dct_coefficients
from quantize_dct_coefficients import quant_matrix1
from ycbcr_to_rgb import convert_ycbcr_to_rgb


def huffman_decompression(encoded_str, huffman_tree, shape, quant_matrix=quant_matrix1):
    # Decode the encoded string
    decoded_coefficients = huffman_decode(encoded_str, huffman_tree, shape)

    # Inverse quantize the DCT coefficients
    dequantized_coefficients = inverse_quantize_dct_coefficients(decoded_coefficients, quant_matrix)

    # Apply inverse DCT on each block
    reconstructed_image = inverse_dct_on_blocks(dequantized_coefficients)

    # Convert YCbCr back to RGB
    rgb_image = convert_ycbcr_to_rgb(reconstructed_image)

    return rgb_image
