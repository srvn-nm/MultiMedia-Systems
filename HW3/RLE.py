import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

# Reading the image
image_path = 'RLE_src.jpg'
image = Image.open(image_path).convert('1')  # Convert the image to binary (black and white)
image_array = np.array(image)

# Display the original image
plt.imshow(image_array, cmap='gray')
plt.title('Original Image')
plt.show()

# Saving the original image
original_image = Image.fromarray(image_array)
original_image.save('original_image.png')


# implementing the RLE compression algorithm
def rle_encode(image_array):
    pixels = image_array.flatten()
    encoded_pixels = []
    current_pixel = pixels[0]
    count = 1

    for pixel in pixels[1:]:
        if pixel == current_pixel:
            count += 1
        else:
            encoded_pixels.append((current_pixel, count))
            current_pixel = pixel
            count = 1
    encoded_pixels.append((current_pixel, count))

    return encoded_pixels


# Compressing the image
encoded_image = rle_encode(image_array)
print("Encoded Image:", encoded_image)


# decoding the compressed image
def rle_decode(encoded_image, shape):
    decoded_pixels = []

    for pixel, count in encoded_image:
        decoded_pixels.extend([pixel] * count)

    decoded_image_array = np.array(decoded_pixels).reshape(shape)
    return decoded_image_array


# Decoding the image
decoded_image_array = rle_decode(encoded_image, image_array.shape)

# Display the decoded image
plt.imshow(decoded_image_array, cmap='gray')
plt.title('Decoded Image')
plt.show()

# Saving the decoded image
decoded_image = Image.fromarray(decoded_image_array)
decoded_image.save('decoded_image.png')

# Compare the images
comparison = np.array_equal(image_array, decoded_image_array)
print("Images are identical:", comparison)
