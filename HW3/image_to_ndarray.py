import cv2


def read_image_to_ndarray(image_path):
    # Read the image using OpenCV
    image = cv2.imread(image_path)

    # Check if the image was successfully read
    if image is None:
        raise ValueError(f"Image not found at {image_path}.")

    # Convert from BGR (default OpenCV format) to RGB
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    return image

