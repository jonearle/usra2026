import sys
import geopandas as gpd
import random
from shapely import Point

# Get .geojson file from command line
if len(sys.argv) < 3:
    print("Please provide a .geojson file and the number of coordinates\n " \
    "Example: python3 geojson-generate-coords.py place.geojson")
    sys.exit(1)
elif len(sys.argv) > 3:
    print("Provided too many arguments")
    sys.exit(1)

fname = sys.argv[1]
num_coords = sys.argv[2]

# Read geojson file
data = gpd.read_file(fname)
if len(data.geometry.iloc) != 1:
    raise ValueError("There is not exactly 1 polygon in the file")
else:
    polygon = data.geometry.iloc[0]
if data.empty:
    raise ValueError("Expected one feature, got none")
if len(data) != 1:
    raise ValueError("Expected one feature, got more")

# creating bounding box 
min_x, min_y, max_x, max_y = polygon.bounds

# Randomaly generate coordinates within bounding box
gen_coords = []
for i in range(0, num_coords):
    while True:
        lon = random.uniform(min_x, max_x)
        lat = random.uniform(min_y, max_y)
        coordinate = Point(lat, lon)
        if polygon.covers(coordinate):
            break
    gen_coords.append(coordinate)

# Convert coordinates to work on a cartesian plane based on the center of all geojson coordinates
