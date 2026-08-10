import folium
import csv

map = folium.Map(location=[44.6488, -63.5930], zoom_start=5)

routeCoordinates = []

with open("/Users/Jon/usra2026/data/bike_comparison_test/meshcore.csv", mode='r') as file:
    reader = csv.DictReader(file)
    next(reader) # skip header

    for row in reader:
        lat = float(row['lat'])
        long = float(row['long'])
        rssi = float(row['rssi'])

        if rssi > -70:
            color = "darkgreen"
        elif rssi > -80:
            color = "limegreen"
        elif rssi > -90:
            color = "yellowgreen"
        elif rssi > -100:
            color = "gold"
        elif rssi > -110:
            color = "orange"
        elif rssi > -120:
            color = "darkorange"
        elif rssi > -130:
            color = "red"
        else:
            color = "darkred"

        folium.CircleMarker(
            location=[lat, long],
            radius=6,
            color=color,
            fill=True,
            fill_color=color,
            fill_opacity=1.0
        ).add_to(map)
    
map.save("/Users/Jon/USRA2026/data/route.html")