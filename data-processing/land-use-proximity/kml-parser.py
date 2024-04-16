import json

# Given KML data
kml_data = None
with open('data.geojson', 'r') as file:
    kml_data = file.read()

# Parse JSON
kml_json_main = json.loads(kml_data)
kml_json_main = kml_json_main['features']

new_data = []

for kml_json in kml_json_main:
    label = kml_json['properties']['Description'].split('<td>')[1].split('<')[0]
    coordinates = kml_json['geometry']['coordinates'][0]

    # Format into desired structure
    formatted_data = {
        'label': label,
        'coordinates': [[coord[1], coord[0]] for coord in coordinates]
    }

    new_data.append(formatted_data)

# Save formatted data
formatted_data = json.dumps(new_data)
with open('formatted-data.json', 'w') as file:
    file.write(formatted_data)