import cv2
import numpy as np
import os

# چک کردن وجود فایل
file_path = 'f.jpg'
if not os.path.exists(file_path):
    print("file is missing.")
    exit()

# خواندن تصویر
image = cv2.imread(file_path)

# تابع تبدیل به grayscale
def rgb_to_gray(image):
    height, width, channels = image.shape
    gray_image = np.zeros((height, width), dtype=np.uint8)
    for y in range(height):
        for x in range(width):
            gray_image[y, x] = int(0.299 * image[y, x, 0] + 0.587 * image[y, x, 1] + 0.114 * image[y, x, 2])
    return gray_image

# تبدیل به grayscale
gray_image = rgb_to_gray(image)

# الگوریتم Floyd-Steinberg Dithering
def floyd_steinberg_dithering(image):
    height, width = image.shape
    for y in range(height):
        for x in range(width):
            old_pixel = image[y, x]
            new_pixel = 255 if old_pixel > 127 else 0
            image[y, x] = new_pixel
            error = old_pixel - new_pixel
            if x < width - 1:
                image[y, x + 1] += error * 7 / 16
            if x > 0 and y < height - 1:
                image[y + 1, x - 1] += error * 3 / 16
            if y < height - 1:
                image[y + 1, x] += error * 5 / 16
            if x < width - 1 and y < height - 1:
                image[y + 1, x + 1] += error * 1 / 16
    return image

# اعمال الگوریتم
dithered_image = floyd_steinberg_dithering(gray_image)

# ذخیره تصویر دیتر شده
cv2.imwrite('FS-dithered.png', dithered_image)
