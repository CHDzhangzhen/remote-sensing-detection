import os
from PIL import Image
import numpy as np
from scipy.spatial import distance
import math
import cv2


threshold_1 =
threshold_2 =
threshold_3 =
threshold_4 =

bbox_folder =
image_folder =


def calculate_distance(coord1, coord2):
    x1, y1 = coord1
    x2, y2 = coord2
    distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    return distance


def calculate_all_distances(coordinates):
    distances = []
    for i in range(len(coordinates) - 1):
        for j in range(i + 1, len(coordinates)):
            distance = calculate_distance(coordinates[i], coordinates[j])
            distances.append(distance)
    return distances



image_files = [f for f in os.listdir(image_folder) if f.endswith('.tif')]
bbox_files = [f for f in os.listdir(bbox_folder) if f.endswith('.txt')]


for bbox_file in bbox_files:

    with open(os.path.join(bbox_folder, bbox_file), 'r') as f:
        bbox_lines = f.readlines()


    image_file = bbox_file.replace('.txt', '.tif')

    filtered_lines = []

    image_path = os.path.join(image_folder, image_file)
    image = Image.open(image_path)
    image_rgb = image.convert('RGB')

    for bbox_line in bbox_lines:

        parts = bbox_line.strip().split()
        x_1 = float(parts[1])
        y = float(parts[2])
        w = float(parts[3])
        h = float(parts[4])


        left = int((x_1 - w / 2) * image.width)
        top = int((y - h / 2) * image.height)
        right = int((x_1 + w / 2) * image.width)
        bottom = int((y + h / 2) * image.height)

        count = 0
        for x_1 in range(left, right):
            for y in range(top, bottom):
                r, g, b = image_rgb.getpixel((x_1, y))
                if (r != threshold_1 and threshold_4) and (g != threshold_2 and threshold_4)and( b != threshold_3 and threshold_4):
                    count += 1

        if count >=36 :
            filtered_lines.append(bbox_line)




        with open(bbox_file, "w") as f:
            f.write("".join(filtered_lines))