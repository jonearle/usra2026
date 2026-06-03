import folium
import csv

map = folium.Map(location=[44.6488, -63.5930], zoom_start=11)

routeCoordinates = []

with open("/home/jonearle/usra2026/data/bike_tests/bike_nearby2_long_fast.csv", mode='r') as file:
    reader = csv.DictReader(file)
    next(reader)
    for row in reader:
        lat = float(row['lat'])
        long = float(row['long'])
        point = (lat, long)
        routeCoordinates.append(point)

folium.PolyLine(routeCoordinates).add_to(map)
    
map.save("/home/jonearle/usra2026/data/routes/nearby_long_fast_2.html")