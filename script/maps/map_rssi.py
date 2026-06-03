import folium
import csv

map = folium.Map(location=[44.6488, -63.5930], zoom_start=5)

routeCoordinates = []

with open("/Users/Jon/USRA2026/data/bike_tests/bike_nearby2_long_fast.csv", mode='r') as file:
    reader = csv.DictReader(file)
    next(reader) # skip header

    for row in reader:
        lat = float(row['lat'])
        long = float(row['long'])
        rssi = float(row['rssi'])

        if rssi > -90:
            color = "green"
        elif rssi > -110:
            color = "yellow"
        elif rssi > -130:
            color = "orange"
        else :
            color = "red"

        folium.CircleMarker(
            location=[lat, long],
            radius=6,
            color=color,
            fill=True,
            fill_color=color,
            fill_opacity=1.0
        ).add_to(map)
    
map.save("/Users/Jon/USRA2026/data/routes/rssi/north_long_fast.html")