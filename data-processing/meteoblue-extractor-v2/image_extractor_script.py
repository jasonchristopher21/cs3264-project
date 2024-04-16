import requests
import json
import numpy as np
import pandas as pd

from bs4 import BeautifulSoup
from PIL import Image
from process_image import process_image
from datetime import datetime

print("Starting the Image extractor script ......")
print("uwu with love by Jason")

########################
# ADJUSTABLE VARIABLES #
########################

# URL of HTML page
url = "https://www.meteoblue.com/en/products/cityclimate/heatmaps/singapore"

# Base URL of the image to be downloaded from
img_base_url = "https://static.meteoblue.com/pub/cityclimate/singapore/"

#####################
# UTILITY FUNCTIONS #
#####################


def parse_datetime(date_str):
    # Parse the string to a datetime object
    original_datetime = datetime.fromisoformat(date_str)

    # Extract date and time components
    date_part = original_datetime.strftime("%Y-%m-%d")
    time_part = original_datetime.strftime("%H:%M")

    return date_part, time_part

###############
# MAIN SCRIPT #
###############


print("Fetching the HTML page from the URL: ", url)

# Make a GET request to the URL to get the HTML content
response = requests.get(url)

if response.status_code != 200:
    print("Failed to fetch the page")
    exit()

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(response.content, "html.parser")
script_tag = soup.find(
    'script', string=lambda text: text and 'mb.settings.city' in text)

city_settings = None

# Extract the JavaScript code containing mb.settings.city
if script_tag:
    # Get the text content of the <script> tag
    js_code = script_tag.string

    # Extract mb.settings.city using regex (assuming mb.settings.city is properly defined)
    import re
    match = re.search(r'mb.settings.city\s*=\s*({.*?});', js_code, re.DOTALL)
    if match:
        mb_settings_city_json = match.group(1)
        city_settings = json.loads(mb_settings_city_json)
else:
    print("mb.settings.city not found in the HTML content. Program terminated")
    exit()

print("HTML page successfully fetched and parsed.")

df = pd.DataFrame(
    columns=['Date', 'Time', 'Latitude', 'Longitude', 'Temperature'])

# Extract the image URLs from the city_settings JSON
for item in city_settings['timesteps']:
    # print(item['date'], item['value'], item['legend']['min'])
    image_filename = "images/" + item['value'].split("/")[1] + ".jpg"
    img_url = img_base_url + item['value'] + ".jpg"
    print("Downloading image from URL: ", img_url)
    response = requests.get(img_url)
    if response.status_code != 200:
        print("Failed to download the image. Proceed to the next image URL.")
        continue
    with open(image_filename, 'wb') as image_file:
        image_file.write(response.content)
    print("Image downloaded successfully to: ", image_filename)
    print("Processing image...")
    date, time = parse_datetime(item['date'])
    new_df = process_image(image_filename, date, time,
                           item['legend']['min'], item['legend']['max'])
    df = pd.concat([df, new_df], ignore_index=True)
    print(f"Image {item['value']} processed successfully.")

# Save the extracted data to a CSV file
output_filename = "output.csv"
df.to_csv(output_filename, index=False)

print("Data extracted and saved to: ", output_filename)

print("Image extraction process completed successfully.")
