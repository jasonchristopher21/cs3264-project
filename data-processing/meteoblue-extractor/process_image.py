# Import statements
from PIL import Image
import numpy as np
import pandas as pd

# Lat-long bounds
lat_min = 1.19966
lat_max = 1.47512
long_min = 103.59258
long_max = 104.01814

# Predetermined colors (meteoblue color scale)
colors = [
    "#563853",
    "#5C3959",
    "#763E70",
    "#94438C",
    "#B967B1",
    "#AF72BD",
    "#AA96D7",
    "#A8B8E4",
    "#A7CDE3",
    "#95DBD7",
    "#77CCC6",
    "#76C0CA",
    "#73ABC8",
    "#77A0D0",
    "#639CA7",
    "#5E9B90",
    "#6AA262",
    "#83A933",
    "#ABB033",
    "#CDB933",
    "#EDC233",
    "#FBAF33",
    "#F98A33",
    "#EE6933",
    "#B95233",
    "#974433",
    "#733933"
]

# Utility Functions 

def color_diff(color1, color2):
    return sum([abs(color1[i] - color2[i]) for i in range(3)])

def closest_color(color, color_map):
    min_diff = color_diff(color, color_map[0]['color'])
    min_color = color_map[0]
    min_temp = color_map[0]['temp']
    for i in range(1, len(color_map)):
        diff = color_diff(color, color_map[i]['color'])
        if diff < min_diff:
            min_diff = diff
            min_color = color_map[i]
            min_temp = color_map[i]['temp']
    return min_color, min_temp

def hex_to_rgb(hex):
    return [int(hex[i:i+2], 16) for i in (1, 3, 5)]

colors = [hex_to_rgb(color) for color in colors]

def process_image(image_file, date, time, temp_min, temp_max):
    # Load image as numpy array
    im = Image.open(image_file)
    im = im.convert('RGB')

    # Convert image to numpy array
    data = np.array(im)

    # Image shape
    height = data.shape[0]
    width = data.shape[1]

    df = pd.DataFrame(columns=['Date', 'Time', 'Latitude', 'Longitude', 'Temperature'])
    
    # Assign temperature to colors
    color_map = []

    for i in range(len(colors)):
        temp = temp_min + ((temp_max - temp_min) / (len(colors) - 1)) * i
        obj = {
            'color': colors[i],
            'temp': temp
        }
        color_map.append(obj)

    # Iterate through image and assign temperature values
    for i in range(height):
        for j in range(width):
            if i % 10 == 0 and j % 10 == 0: # Only sample every 4th pixel, cos it's too slow otherwise
                color = data[i][j]
                closest, temp = closest_color(color, color_map)
                lat = lat_min + (lat_max - lat_min) * i / height
                long = long_min + (long_max - long_min) * j / width
                new_df = {
                    'Date': date,
                    'Time': time,
                    'Latitude': lat,
                    'Longitude': long,
                    'Temperature': temp
                }
                df.loc[len(df)] = new_df

    return df