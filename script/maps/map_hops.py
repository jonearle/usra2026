import folium
import csv

map = folium.Map(location=[44.6488, -63.5930], zoom_start=5)

routeCoordinates = []

with open("/Users/Jon/usra2026/data/dynamic_test/dynamic_test_2.csv", mode='r') as file:
    reader = csv.DictReader(file)
    next(reader) # skip header

    for row in reader:
        lat = float(row['lat'])
        long = float(row['long'])
        hops = float(row['hopsUsed'])

        if hops == 0:
            color = "#f0f921"  # bright yellow
        elif hops == 1:
            color = "#fca636"  # orange
        elif hops == 2:
            color = "#e16462"  # salmon
        elif hops == 3:
            color = "#b12a90"  # magenta
        elif hops == 4:
            color = "#6a00a8"  # purple
        else:  # 5+ hops
            color = "#0d0887"  # dark blue

        folium.CircleMarker(
            location=[lat, long],
            radius=6,
            color=color,
            fill=True,
            fill_color=color,
            fill_opacity=1.0
        ).add_to(map)
    
map.save("/Users/Jon/USRA2026/data/route.html")