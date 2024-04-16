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
    subzone = kml_json['properties']['Description'].split('<td>')[2].split('<')[0]
    planning_area = kml_json['properties']['Description'].split('<td>')[5].split('<')[0]
    region = kml_json['properties']['Description'].split('<td>')[7].split('<')[0]

    coordinates = kml_json['geometry']['coordinates'][0]

    # Format into desired structure
    formatted_data = {
        'subzone': subzone,
        'planning_area': planning_area,
        'region': region,
        'coordinates': [[coord[1], coord[0]] for coord in coordinates]
    }

    new_data.append(formatted_data)

# Save formatted data
formatted_data = json.dumps(new_data)
with open('formatted-data.json', 'w') as file:
    file.write(formatted_data)