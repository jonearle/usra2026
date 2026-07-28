import sys
import geopandas as gpd
import random
import math
import yaml
from shapely import MultiPolygon, Point, Polygon, transform

# Get .geojson file from command line
if len(sys.argv) < 3:
    print("Please provide a .geojson file and the number of coordinates\n" \
    "Example: python3 geojson-generate-coords.py place.geojson")
    sys.exit(1)
elif len(sys.argv) > 3:
    print("Provided too many arguments")
    sys.exit(1)

fname = sys.argv[1]
num_coords = int(sys.argv[2])


# Read geojson file
data = gpd.read_file(fname)
if data.shape[0] != 1:
    raise ValueError("There is not exactly 1 object in the file")
elif type(data.geometry.iloc[0]) not in [Polygon, MultiPolygon]:
    raise ValueError("Object is not of type Polygon or MultiPolygon")
else:
    polygon = data.geometry.iloc[0]

# creating bounding box 
min_x, min_y, max_x, max_y = polygon.bounds


# Randomly generate coordinates within bounding box
gen_coords = []
for i in range(0, num_coords):
    while True:
        lon = round(random.uniform(min_x, max_x), 6)
        lat = round(random.uniform(min_y, max_y), 6)
        coordinate = Point(lon, lat)
        if polygon.covers(coordinate):
            break
    gen_coords.append(coordinate)

# Convert coordinates to work on a cartesian plane based on the center of all geojson coordinates
center = polygon.centroid
center = transform(center, lambda coords: coords * (math.pi/180)) 

for point in gen_coords: # Convert to rad and get the vert/hrz distance between point and center
    point = transform(point, lambda coords: coords * (math.pi/180))
    x = (point.x - center.x) * 111320 * math.cos(center.y)
    y = (point.y - center.y) * 111320
    point = Point(x, y)

center = Point(0, 0)

# Turn all coordinates into nodeConfig.yaml
defaults = {
    "antennaGain": 0.0,
    "hopLimit": 3,
    "isClientMute": "false",
    "isRepeater": "false",
    "isRouter": "false",
    "neighborInfo": "false",
    "x": 0,
    "y": 0,
    "z": 1.0
}

for i in range(0, len(gen_coords)): 
    defaults["x"] = gen_coords[i].x
    defaults["y"] = gen_coords[i].y
    config = {i: defaults}

    with open("nodeConfig.yaml", "a") as file:
        yaml.safe_dump(config, file, default_flow_style=False, sort_keys=False)




