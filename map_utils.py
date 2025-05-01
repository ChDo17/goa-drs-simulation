import folium
import pandas as pd
import numpy as np
import geopandas as gpd
from shapely.geometry import Point, box
import streamlit.components.v1 as components

def show_map():
    # 🗺️ Use OpenStreetMap to make roads visible
    m = folium.Map(location=[15.5, 73.8], zoom_start=10, tiles="OpenStreetMap")

    # 🔸 Load Goa boundary
    goa_gdf = gpd.read_file("data/goa_boundary.geojson")
    goa_polygon = goa_gdf.unary_union

    # 🔸 Load collection points and filter only points on land
    try:
        df = pd.read_csv("data/collection_points.csv")
        df['geometry'] = df.apply(lambda row: Point(row['longitude'], row['latitude']), axis=1)
        gdf = gpd.GeoDataFrame(df, geometry='geometry')
        points_on_land = gdf[gdf.geometry.within(goa_polygon)]

        # 🔲 Square marker for each point (color based on category)
        for _, row in points_on_land.iterrows():
            color = {
                'hotel': 'blue',
                'kirana': 'purple',
                'cafe': 'orange',
                'bar': 'red'
            }.get(row['category'], 'gray')

            folium.Marker(
                location=[row['latitude'], row['longitude']],
                icon=folium.DivIcon(html=f"""
                    <div style='width:10px;height:10px;background:{color};'></div>
                """)
            ).add_to(m)
    except Exception as e:
        print("Error loading points:", e)

    # 🔳 Grid overlay (1km x 1km) clipped to Goa land
    lat_min, lat_max = 14.9, 15.9
    lon_min, lon_max = 73.7, 74.3
    lat_step, lon_step = 0.009, 0.009  # approx 1km

    for lat in np.arange(lat_min, lat_max, lat_step):
        for lon in np.arange(lon_min, lon_max, lon_step):
            grid_cell = box(lon, lat, lon + lon_step, lat + lat_step)
            if grid_cell.intersects(goa_polygon):
                bounds = [[lat, lon], [lat + lat_step, lon], [lat + lat_step, lon + lon_step], [lat, lon + lon_step], [lat, lon]]
                folium.PolyLine(bounds, color="green", weight=0.5, opacity=0.4).add_to(m)

    # 📍 Show map inside Streamlit
    components.html(m._repr_html_(), height=600)
