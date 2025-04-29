import os
import cv2
import numpy as np


def load_image(file_path, target_rgbs):

    image = cv2.imread(file_path)


    target_rgbs = [np.array(rgb) for rgb in target_rgbs]


    mask = np.zeros_like(image)

    for target_rgb in target_rgbs:
        mask[(image == target_rgb).all(axis=2)] = [255, 255, 255]

    mask[(image != target_rgbs[0]).any(axis=2) & (image != target_rgbs[1]).any(axis=2)] = [0, 0, 0]

    return image, mask


def find_connected_components(image, mask):
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Thresholding
    _, binary = cv2.threshold(gray, 1, 255, cv2.THRESH_BINARY)

    # Apply the mask to the binary image
    masked_binary = cv2.bitwise_and(binary, mask[:, :, 0])

    # Invert the masked binary image
    masked_binary_inverted = cv2.bitwise_not(masked_binary)

    # Connected components analysis
    num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(masked_binary_inverted, connectivity=8)

    return num_labels, labels, stats, centroids


def process_images(input_folder, output_folder, target_rgbs):

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)


    for filename in os.listdir(input_folder):
        if filename.endswith(".tif"):

            input_path = os.path.join(input_folder, filename)


            image, mask = load_image(input_path, target_rgbs)

            # Connected components analysis
            num_labels, labels, stats, centroids = find_connected_components(image, mask)

            # Modify labels
            for i in range(num_labels):
                label_mask = (labels == i)
                # If label is 0 or the connected component size is less than 5, set the pixels to [0, 230, 76]
                if i == 0 or np.sum(label_mask) < 30:
                    image[label_mask] = [0, 230, 76]


            output_path = os.path.join(output_folder, filename)


            cv2.imwrite(output_path, image)

            print(f"Processed: {filename}")


# Define target RGB value
target_rgbs = [[0, 230, 76], [255, 255, 255]]



# 处理图像
process_images(input_folder, output_folder, target_rgbs)