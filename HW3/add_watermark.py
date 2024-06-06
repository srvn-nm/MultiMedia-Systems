def add_watermark(image, watermark_data):
    """
    Add a reversible watermark to the image using the LSB method.

    Parameters:
    image (np.ndarray): Input image array.
    watermark_data (str): Watermark data to embed.

    Returns:
    np.ndarray: Watermarked image.
    """
    watermark_bits = [int(bit) for bit in watermark_data]
    flat_image = image.flatten()

    for i, bit in enumerate(watermark_bits):
        flat_image[i] = (flat_image[i] & ~1) | bit  # Set the LSB to the watermark bit

    watermarked_image = flat_image.reshape(image.shape)
    return watermarked_image
