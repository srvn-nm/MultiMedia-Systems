import cv2
import numpy as np

# خواندن تصویر
image = cv2.imread('s.jpg')

# تبدیل تصویر به grayscale
def rgb_to_gray(image):
    gray_image = np.zeros((image.shape[0], image.shape[1]), dtype=np.uint8)
    for y in range(image.shape[0]):
        for x in range(image.shape[1]):
            gray_image[y, x] = int(0.299 * image[y, x, 0] + 0.587 * image[y, x, 1] + 0.114 * image[y, x, 2])
    return gray_image

gray_image = rgb_to_gray(image)

# ذخیره تصویر grayscale
cv2.imwrite('grayscale.png', gray_image)

# ماتریس دیترینگ
dither_matrix = np.array([[0, 8, 2, 10],
                          [12, 4, 14, 6],
                          [3, 11, 1, 9],
                          [15, 7, 13, 5]])

# اندازه تصویر
height, width = gray_image.shape

# اعمال الگوریتم دیترینگ
for y in range(height):
    for x in range(width):
        old_pixel = gray_image[y, x]
        new_pixel = 255 if old_pixel > dither_matrix[y % 4, x % 4] * 16 else 0
        gray_image[y, x] = new_pixel

# ذخیره تصویر دیتر شده
cv2.imwrite('o_dithered.png', gray_image)
