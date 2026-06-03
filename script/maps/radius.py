import folium

# Goldberg coords: 44.63750061681808, -63.58725771856945
map = folium.Map(location=[44.63750061681808, -63.58725771856945], zoom_start=15)

# Approx radius w/ buildings: 175m
# Approx radius down street: 250m
folium.Circle(
            location=[44.63750061681808, -63.58725771856945],
            radius=175,
            color="green",
            fill=True,
            fill_opacity=0.3
        ).add_to(map)

map.save("/Users/Jon/USRA2026/data/routes/radius/short_turbo_buildings.html")


