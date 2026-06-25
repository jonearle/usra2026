import os
import io
import rasterio
import pandas as pd
import geopandas as gpd
import contextily as ctx
import matplotlib.pyplot as plt
from pptx import Presentation
from pptx.util import Inches
from rasterio.plot import show

df = pd.read_csv("/Users/Jon/usra2026/data/retransmission/retransmission_deltas.csv")

map_path = "/Users/Jon/usra2026/data/campus.tif"

gdf = gpd.GeoDataFrame(
    df, 
    geometry=gpd.points_from_xy(df['longitude'], df['latitude']),
    crs="EPSG:4326"
    )
gdf = gdf.to_crs(epsg=3857)

if not os.path.exists(map_path):
    ctx.bounds2raster(
        *gdf.total_bounds,
        zoom=16,
        path=map_path,
        source=ctx.providers.Esri.WorldGrayCanvas
    )

fig, ax = plt.subplots(figsize=(10, 10))
with rasterio.open(map_path) as src:
    show(src, ax=ax)

gdf.plot(ax=ax, column='numPacketsTxDelta', cmap='coolwarm', markersize=100, legend=True)
ax.set_axis_off()
plt.title("Meshtastic Retransmission Test Results")
plt.show()
