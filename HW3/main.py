import cv2
import numpy as np
from matplotlib import pyplot as plt

from HuffmanNode import huffman_decode, huffman_encode, generate_huffman_codes, build_huffman_tree
from PSNR_SSIM import calculate_compression_ratio, calculate_quality_metrics
from add_watermark import add_watermark
from arithmetic_decode import arithmetic_decode
from arithmetic_encode import arithmetic_encode
from dct_on_blocks import dct_on_blocks
from image_to_ndarray import read_image_to_ndarray
from inverse_dct_on_blocks import inverse_dct_on_blocks
from inverse_quantize_dct_coefficients import inverse_quantize_dct_coefficients
from pad_image_to_multiple_of_8 import pad_image_to_multiple_of_8
from quantize_dct_coefficients import quantize_dct_coefficients, quant_matrix1, quant_matrix3, quant_matrix2
from remove_watermark import remove_watermark
from rgb_to_ycbcr import convert_rgb_to_ycbcr
from ycbcr_to_rgb import convert_ycbcr_to_rgb


def main(image_path, quant_matrix=quant_matrix1, compression_method='huffman', color_space='YCbCr',
         watermark_data=None):
    # Read the image
    image = read_image_to_ndarray(image_path)
    image = pad_image_to_multiple_of_8(image)  # Ensure the image dimensions are divisible by 8

    if watermark_data:
        image = add_watermark(image, watermark_data)

    transformed_image = None
    decoded_coefficients = None
    final_image = None
    compressed_size = None
    reconstructed_image = None

    if color_space == 'YCbCr':
        # Convert RGB to YCbCr
        transformed_image = convert_rgb_to_ycbcr(image)
    elif color_space == 'HSV':
        # Convert RGB to HSV
        hsv_image = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
        transformed_image = np.transpose(hsv_image, (2, 0, 1))

    transformed_image = pad_image_to_multiple_of_8(transformed_image)  # Ensure the transformed image is padded

    # Apply DCT on each block
    dct_coefficients = dct_on_blocks(transformed_image)

    # Quantize the DCT coefficients
    quantized_coefficients = quantize_dct_coefficients(dct_coefficients, quant_matrix)

    if compression_method == 'huffman':
        # Build Huffman Tree
        huffman_tree = build_huffman_tree(quantized_coefficients)

        # Generate Huffman codes
        huffman_codebook = generate_huffman_codes(huffman_tree)

        # Encode DCT coefficients
        encoded_str = huffman_encode(quantized_coefficients, huffman_codebook)
        compressed_size = len(encoded_str)
        # Decode the encoded string
        decoded_coefficients = huffman_decode(encoded_str, huffman_tree, quantized_coefficients.shape)
    elif compression_method == 'arithmetic':
        encoded_image, model = arithmetic_encode(quantized_coefficients)
        compressed_size = len(encoded_image)
        decoded_coefficients = arithmetic_decode(encoded_image, model, quantized_coefficients.shape)

    if decoded_coefficients is not None:
        # Inverse quantize the DCT coefficients
        dequantized_coefficients = inverse_quantize_dct_coefficients(decoded_coefficients, quant_matrix)

        # Apply inverse DCT on each block
        reconstructed_image = inverse_dct_on_blocks(dequantized_coefficients)

    if color_space == 'YCbCr':
        # Convert YCbCr back to RGB
        final_image = convert_ycbcr_to_rgb(reconstructed_image)
    elif color_space == 'HSV':
        # Convert HSV back to RGB
        hsv_image_reconstructed = np.transpose(reconstructed_image, (1, 2, 0))
        final_image = cv2.cvtColor(hsv_image_reconstructed, cv2.COLOR_HSV2RGB)

    if watermark_data:
        final_image, extracted_watermark = remove_watermark(final_image)
        print(f'Extracted Watermark: {extracted_watermark}')

    compression_ratio = calculate_compression_ratio(image, compressed_size)
    psnr_value, ssim_value = calculate_quality_metrics(image, final_image)

    return final_image, compression_ratio, psnr_value, ssim_value


# testing
# Define the quantization matrices and color spaces to test
quant_matrices = [quant_matrix1, quant_matrix2, quant_matrix3]
color_spaces = ['YCbCr', 'HSV']
# Example usage with watermarking and arithmetic coding
watermark_data = '1010101010101010'  # Example watermark data
if __name__ == "__main__":
    # Test with different quantization matrices
    for quant_matrix in quant_matrices:
        compressed_image, compression_ratio, psnr_value, ssim_value = main('image.jpg', quant_matrix=quant_matrix,
                                                                           watermark_data=watermark_data)
        print(f'Quantization Matrix:\n{quant_matrix}')
        print(f'Compression Ratio: {compression_ratio}')
        print(f'PSNR: {psnr_value}')
        print(f'SSIM: {ssim_value}')
        plt.imshow(compressed_image)
        plt.title(f'Compressed Image with PSNR: {psnr_value} and SSIM: {ssim_value}')
        plt.show()

    # Test with different color spaces
    for color_space in color_spaces:
        compressed_image, compression_ratio, psnr_value, ssim_value = main('image.jpg', color_space=color_space,
                                                                           watermark_data=watermark_data)
        print(f'Color Space: {color_space}')
        print(f'Compression Ratio: {compression_ratio}')
        print(f'PSNR: {psnr_value}')
        print(f'SSIM: {ssim_value}')
        plt.imshow(compressed_image)
        plt.title(f'Compressed Image with PSNR: {psnr_value} and SSIM: {ssim_value}')
        plt.show()
