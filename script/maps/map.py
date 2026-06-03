import folium
import csv

map = folium.Map(location=[44.6488, -63.5930], zoom_start=11)

routeCoordinates = []

with open("/Users/Jon/USRA2026/data/bike_tests/bike_north_long_fast_fail.csv", mode='r') as file:
    reader = csv.DictReader(file)
    next(reader)
    for row in reader:
        lat = float(row['lat'])
        long = float(row['long'])
        point = (lat, long)
        routeCoordinates.append(point)

folium.PolyLine(routeCoordinates).add_to(map)
    
map.save("/Users/Jon/USRA2026/data/routes/desk.html")