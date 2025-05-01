import folium
import pandas as pd
import numpy as np
import geopandas as gpd
from shapely.geometry import Point, box
import streamlit.components.v1 as components

def show_map():
    m = folium.Map(location=[15.5, 73.8], zoom_start=10, tiles="OpenStreetMap")

    # --- Load Goa Boundary (GeoJSON) ---
    try:
        goa_boundary = gpd.read_file("data/goa_boundary.geojson")
        goa_polygon = goa_boundary.unary_union
    except:
        st.error("Goa boundary file not found!")
        return

    # --- Load Collection Points ---
    try:
        df = pd.read_csv("data/collection_points.csv")
        df['geometry'] = df.apply(lambda row: Point(row['longitude'], row['latitude']), axis=1)
        gdf = gpd.GeoDataFrame(df, geometry='geometry')
        points_on_land = gdf[gdf.geometry.within(goa_polygon)]

        for _, row in points_on_land.iterrows():
            color = {
                'hotel': 'blue',
                'kirana': 'purple',
                'cafe': 'orange',
                'bar': 'red'
            }.get(row['category'], 'gray')

            # --- Use square-shaped marker using DivIcon ---
            folium.Marker(
                location=[row['latitude'], row['longitude']],
                icon=folium.DivIcon(html=f"""
                    <div style='width:12px;height:12px;background:{color};opacity:0.8;border-radius:2px;'></div>
                """)
            ).add_to(m)
    except:
        st.error("Error loading collection points")

    # --- Draw 1km² Grid, but only over Goa land ---
    lat_min, lat_max = 14.9, 15.9
    lon_min, lon_max = 73.7, 74.3
    lat_step = 0.009
    lon_step = 0.009

    for lat in np.arange(lat_min, lat_max, lat_step):
        for lon in np.arange(lon_min, lon_max, lon_step):
            grid_cell = box(lon, lat, lon + lon_step, lat + lat_step)
            if grid_cell.intersects(goa_polygon):
                bounds = [[lat, lon], [lat + lat_step, lon], 
                          [lat + lat_step, lon + lon_step], 
                          [lat, lon + lon_step], [lat, lon]]
                folium.PolyLine(bounds, color="green", weight=0.4, opacity=0.3).add_to(m)

    # --- Render map inside Streamlit ---
    components.html(m._repr_html_(), height=600)
