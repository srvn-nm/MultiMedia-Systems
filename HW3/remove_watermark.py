def remove_watermark(image):
    """
    Remove the reversible watermark from the image and extract the watermark data.

    Parameters:
    image (np.ndarray): Watermarked image array.

    Returns:
    np.ndarray: Image without watermark.
    str: Extracted watermark data.
    """
    flat_image = image.flatten()
    extracted_bits = [flat_image[i] & 1 for i in range(len(flat_image))]
    watermark_data = ''.join(map(str, extracted_bits))

    original_image = (flat_image & ~1).reshape(image.shape)  # Reset the LSB to 0
    return original_image, watermark_data
