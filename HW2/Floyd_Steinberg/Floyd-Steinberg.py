import cv2
import numpy as np

# خواندن تصویر
image = cv2.imread('1665__girl_with_a_pearl_earring_sm.jpg')

# تبدیل تصویر به grayscale
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# اعمال الگوریتم Floyd-Steinberg Dithering
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

# اجرای الگوریتم Floyd-Steinberg Dithering
dithered_image = floyd_steinberg_dithering(gray_image)

# ذخیره تصویر دیتر شده
cv2.imwrite('FS-dithered.png', dithered_image)
