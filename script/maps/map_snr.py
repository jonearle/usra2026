import folium
import csv

map = folium.Map(location=[44.6488, -63.5930], zoom_start=5)

routeCoordinates = []

with open("/Users/Jon/USRA2026/data/bike_comparison_test/meshcore.csv", mode='r') as file:
    reader = csv.DictReader(file)
    next(reader) # skip header

    for row in reader:
        lat = float(row['lat'])
        long = float(row['long'])
        snr = float(row['snr'])

        if snr > 10:
            color = "darkgreen"
        elif snr > 5:
            color = "green"
        elif snr > 0:
            color = "yellow"
        elif snr > -5:
            color = "orange"
        elif snr > -10:
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