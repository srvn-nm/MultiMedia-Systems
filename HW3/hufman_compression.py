from HuffmanNode import build_huffman_tree, generate_huffman_codes, huffman_encode
from dct_on_blocks import dct_on_blocks
from quantize_dct_coefficients import quant_matrix1, quantize_dct_coefficients
from rgb_to_ycbcr import convert_rgb_to_ycbcr


def huffman_compression(image, quant_matrix=quant_matrix1):
    # Convert RGB to YCbCr
    ycbcr_image = convert_rgb_to_ycbcr(image)

    # Apply DCT on each block
    dct_coefficients = dct_on_blocks(ycbcr_image)

    # Quantize the DCT coefficients
    quantized_coefficients = quantize_dct_coefficients(dct_coefficients, quant_matrix)

    # Build Huffman Tree
    huffman_tree = build_huffman_tree(quantized_coefficients)

    # Generate Huffman codes
    huffman_codebook = generate_huffman_codes(huffman_tree)

    # Encode DCT coefficients
    encoded_str = huffman_encode(quantized_coefficients, huffman_codebook)

    return encoded_str, huffman_tree, quantized_coefficients.shape, huffman_codebook
