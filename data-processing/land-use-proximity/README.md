# Land Use and Proximity Data

This folder leverages the previous coordinates returned by the Meteoblue Extractor to determine the land use data (since the land use data is given as a polygonal GeoJSON file from URA), and to determine the proximity to nearby green spaces and water bodies, also basing on the land use dataset provided.

You may need to install the `shapely` library which is use for the geometry processing

Link to dataset:
[https://beta.data.gov.sg/datasets/d_90d86daa5bfaa371668b84fa5f01424f/view](https://beta.data.gov.sg/datasets/d_90d86daa5bfaa371668b84fa5f01424f/view)

## Files Overview

### Elevations Extractor

The `elevations-extractor.ipynb` file interacts with the Open Elevations api ([https://open-elevation.com/](https://open-elevation.com/)), which performs a `POST` request and returns a CSV file containing the elevation data w.r.t. the provided coordinates

### Land use and Proximity Extractor

The `land-use-extractor.ipynb` file preprocesses the provided [Master Plan 2019 GeoJSON file](./data.geojson), and **for each coordinate returned by the Meteoblue Extractor**, determines:

1. The land use label (e.g. WATERBODY or BUSINESS, etc.). If the land use is out of bounds in the Master Plan, an UNKNOWN label is returned instead

2. The distance between the specified coordinate to the closest WATERBODY labeled land area

3. The distance between the specified coordinate to the closest OPEN SPACE **or** PARK labeled land area

### Combination

The elevations and land use and proximity files are combined together manually as a CSV file (since at this point i'm lazy to write the CSV code out. If I can MS Excel it, why not :V)