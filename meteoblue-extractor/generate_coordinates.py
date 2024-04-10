# Import statements
from PIL import Image
import numpy as np
import json

# Lat-long bounds
lat_min = 1.19966
lat_max = 1.47512
long_min = 103.59258
long_max = 104.01814

def gen_coord(image_file):
    # Load image as numpy array
    im = Image.open(image_file)
    im = im.convert('RGB')

    # Convert image to numpy array
    data = np.array(im)

    # Image shape
    height = data.shape[0]
    width = data.shape[1]

    pairs = []

    # Iterate through image and assign temperature values
    for i in range(height):
        for j in range(width):
            if i % 10 == 0 and j % 10 == 0: # Only sample every 4th pixel, cos it's too slow otherwise
                lat = lat_min + (lat_max - lat_min) * i / height
                long = long_min + (long_max - long_min) * j / width
                pairs.append([lat, long])

    with open("coordinates.json", "w") as file:
        file.write(json.dumps(pairs))

if __name__ == "__main__":
    gen_coord("singapore_2024040910.jpg")