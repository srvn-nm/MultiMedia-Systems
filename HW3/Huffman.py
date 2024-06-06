import heapq
from collections import Counter
import cv2
import matplotlib.pyplot as plt
import numpy as np


# reading image
def read_image(image_path):
    image = cv2.imread(image_path)
    return image


# transformation of color spaces
def rgb_to_ycbcr(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2YCrCb)


def ycbcr_to_rgb(image):
    return cv2.cvtColor(image, cv2.COLOR_YCrCb2BGR)


def rgb_to_hsv(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2HSV)


def hsv_to_rgb(image):
    return cv2.cvtColor(image, cv2.COLOR_HSV2BGR)


# Dividing into 8x8 blocks and Discrete Cosine Transform (DCT)
def blockify(image, block_size=8):
    h, w, c = image.shape
    blocks = []
    for channel in range(c):
        channel_blocks = []
        for i in range(0, h, block_size):
            for j in range(0, w, block_size):
                block = image[i:i + block_size, j:j + block_size, channel]
                if block.shape == (block_size, block_size):
                    channel_blocks.append(block)
        blocks.append(channel_blocks)
    return blocks


def dct_block(block):
    return cv2.dct(block.astype(np.float32))


def apply_dct(blocks):
    dct_blocks = []
    for channel_blocks in blocks:
        channel_dct_blocks = [dct_block(block) for block in channel_blocks]
        dct_blocks.append(channel_dct_blocks)
    return dct_blocks


# Quantization of DCT coefficients
default_quantization_matrix = np.array([
    [16, 11, 10, 16, 24, 40, 51, 61],
    [12, 12, 14, 19, 26, 58, 60, 55],
    [14, 13, 16, 24, 40, 57, 69, 56],
    [14, 17, 22, 29, 51, 87, 80, 62],
    [18, 22, 37, 56, 68, 109, 103, 77],
    [24, 35, 55, 64, 81, 104, 113, 92],
    [49, 64, 78, 87, 103, 121, 120, 101],
    [72, 92, 95, 98, 112, 100, 103, 99]])


def quantize_block(block, quant_matrix):
    return np.round(block / quant_matrix).astype(np.int32)


def apply_quantization(dct_blocks, quant_matrix):
    quantized_blocks = []
    for channel_blocks in dct_blocks:
        channel_quantized_blocks = [quantize_block(block, quant_matrix) for block in channel_blocks]
        quantized_blocks.append(channel_quantized_blocks)
    return quantized_blocks


# Huffman tree construction and dynamic coding
class Node:
    def __init__(self, freq, symbol, left=None, right=None):
        self.freq = freq
        self.symbol = symbol
        self.left = left
        self.right = right
        self.huff = ''


def create_huffman_tree(data):
    frequencies = Counter(data)
    heap = [[weight, [symbol, ""]] for symbol, weight in frequencies.items()]
    heapq.heapify(heap)
    while len(heap) > 1:
        lo = heapq.heappop(heap)
        hi = heapq.heappop(heap)
        for pair in lo[1:]:
            pair[1] = '0' + pair[1]
        for pair in hi[1:]:
            pair[1] = '1' + pair[1]
        heapq.heappush(heap, [lo[0] + hi[0]] + lo[1:] + hi[1:])
    huffman_tree = sorted(heapq.heappop(heap)[1:], key=lambda p: (len(p[-1]), p))
    return huffman_tree


def huffman_encode(data, huffman_tree):
    huff_dict = {symbol: code for symbol, code in huffman_tree}
    encoded_data = "".join(huff_dict[symbol] for symbol in data)
    return encoded_data, huff_dict


def huffman_decode(encoded_data, huff_dict):
    reverse_huff_dict = {v: k for k, v in huff_dict.items()}
    decoded_data = []
    current_code = ""
    for bit in encoded_data:
        current_code += bit
        if current_code in reverse_huff_dict:
            decoded_data.append(reverse_huff_dict[current_code])
            current_code = ""
    return decoded_data


def flatten_blocks(blocks):
    flattened = []
    for channel_blocks in blocks:
        for block in channel_blocks:
            flattened.extend(block.flatten())
    return flattened


def deflatten_blocks(data, original_blocks):
    block_size = original_blocks[0][0].shape[0]
    new_blocks = []
    idx = 0
    for channel_blocks in original_blocks:
        channel_new_blocks = []
        for block in channel_blocks:
            flat_block = data[idx:idx + block_size * block_size]
            new_block = np.array(flat_block).reshape((block_size, block_size))
            channel_new_blocks.append(new_block)
            idx += block_size * block_size
        new_blocks.append(channel_new_blocks)
    return new_blocks


# Inverse quantization and inverse DCT transform
def dequantize_block(block, quant_matrix):
    return (block * quant_matrix).astype(np.float32)


def apply_dequantization(quantized_blocks, quant_matrix):
    dequantized_blocks = []
    for channel_blocks in quantized_blocks:
        channel_dequantized_blocks = [dequantize_block(block, quant_matrix) for block in channel_blocks]
        dequantized_blocks.append(channel_dequantized_blocks)
    return dequantized_blocks


def idct_block(block):
    return cv2.idct(block)


def apply_idct(dct_blocks):
    idct_blocks = []
    for channel_blocks in dct_blocks:
        channel_idct_blocks = [idct_block(block) for block in channel_blocks]
        idct_blocks.append(channel_idct_blocks)
    return idct_blocks


# Image reconstruction and inverse color space conversion
def reconstruct_image(blocks, image_shape, block_size=8):
    h, w, c = image_shape
    reconstructed_image = np.zeros(image_shape, dtype=np.uint8)
    for channel in range(c):
        idx = 0
        for i in range(0, h, block_size):
            for j in range(0, w, block_size):
                if idx < len(blocks[channel]):
                    reconstructed_image[i:i + block_size, j:j + block_size, channel] = np.clip(blocks[channel][idx], 0,
                                                                                               255)
                    idx += 1
    return reconstructed_image


# Reversible watermark implementation
def add_watermark(blocks, watermark_data):
    watermarked_blocks = []
    watermark_len = len(watermark_data)
    for i, channel_blocks in enumerate(blocks):
        channel_watermarked_blocks = []
        for j, block in enumerate(channel_blocks):
            if i == 0 and j < watermark_len:
                block[0, 0] = watermark_data[j]
            channel_watermarked_blocks.append(block)
        watermarked_blocks.append(channel_watermarked_blocks)
    return watermarked_blocks


def extract_watermark(blocks, watermark_len):
    extracted_watermark = []
    for i, channel_blocks in enumerate(blocks):
        if i == 0:
            for j in range(watermark_len):
                extracted_watermark.append(blocks[i][j][0, 0])
    return extracted_watermark


# Visualization implementation of DCT coefficients and Huffman tree
def visualize_dct(blocks, title="DCT Coefficients"):
    fig, axs = plt.subplots(1, len(blocks), figsize=(20, 5))
    for i, channel_blocks in enumerate(blocks):
        axs[i].imshow(np.log(np.abs(channel_blocks[0]) + 1), cmap='gray')
        axs[i].set_title(f"Channel {i}")
    plt.suptitle(title)
    plt.show()


def visualize_huffman_tree(huffman_tree):
    for symbol, code in huffman_tree:
        print(f"Symbol: {symbol}, Code: {code}")


# display the image
def display_image(image, title='Image'):
    plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    plt.title(title)
    plt.axis('off')
    plt.show()


def main(image_path, quantization_matrix=default_quantization_matrix, color_space='ycbcr', watermark_data=None):
    # Step 1: Read the image
    image = read_image(image_path)

    # Step 2: Convert the color space
    if color_space == 'ycbcr':
        converted_image = rgb_to_ycbcr(image)
    elif color_space == 'hsv':
        converted_image = rgb_to_hsv(image)
    else:
        raise ValueError("Unsupported color space")

    # Step 3: Divide into blocks and apply DCT
    blocks = blockify(converted_image)
    dct_blocks = apply_dct(blocks)

    # Visualization of DCT coefficients
    visualize_dct(dct_blocks, "Original DCT Coefficients")

    # Step 4: Apply quantization
    quantized_blocks = apply_quantization(dct_blocks, quantization_matrix)

    # Step 5: Add watermark if provided
    if watermark_data is not None:
        quantized_blocks = add_watermark(quantized_blocks, watermark_data)

    # Flatten and Huffman encode
    flattened_quantized_blocks = flatten_blocks(quantized_blocks)
    huffman_tree = create_huffman_tree(flattened_quantized_blocks)
    encoded_data, huff_dict = huffman_encode(flattened_quantized_blocks, huffman_tree)

    # Visualization of Huffman Tree
    visualize_huffman_tree(huffman_tree)

    # Decode and reconstruct blocks
    decoded_data = huffman_decode(encoded_data, huff_dict)
    decoded_blocks = deflatten_blocks(decoded_data, blocks)

    # Extract watermark if provided
    if watermark_data is not None:
        extracted_watermark = extract_watermark(decoded_blocks, len(watermark_data))
        print("Extracted Watermark:", extracted_watermark)

    # Dequantization and apply IDCT
    dequantized_blocks = apply_dequantization(decoded_blocks, quantization_matrix)
    idct_blocks = apply_idct(dequantized_blocks)

    # Visualization of Dequantized DCT coefficients
    visualize_dct(idct_blocks, "Dequantized DCT Coefficients")

    # Reconstruct the image
    reconstructed_image = reconstruct_image(idct_blocks, image.shape)

    # Convert back to original color space
    if color_space == 'ycbcr':
        final_image = ycbcr_to_rgb(reconstructed_image)
    elif color_space == 'hsv':
        final_image = hsv_to_rgb(reconstructed_image)

    # Display images
    display_image(image, 'Original Image')
    display_image(final_image, 'Compressed Image')


if __name__ == "__main__":
    main('image.jpg', watermark_data=[1, 2, 3])
