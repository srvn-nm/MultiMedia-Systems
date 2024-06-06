from skimage.metrics import peak_signal_noise_ratio as psnr, structural_similarity as ssim


def calculate_compression_ratio(original_image, compressed_size):
    # original_size = original_image.size * original_image.itemsize
    original_size = original_image.size * 8  # assuming 8 bits per pixel
    return original_size / compressed_size


def calculate_quality_metrics(original_image, reconstructed_image):
    psnr_value = psnr(original_image, reconstructed_image, data_range=original_image.max() - original_image.min())
    ssim_value = ssim(original_image, reconstructed_image, multichannel=True)
    return psnr_value, ssim_value
