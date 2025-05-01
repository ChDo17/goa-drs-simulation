import folium
import pandas as pd
import numpy as np
import streamlit.components.v1 as components

def show_map():
    # Base map
    m = folium.Map(location=[15.5, 73.8], zoom_start=10, tiles="CartoDB dark_matter")

    # ---- 1. Plot collection points ----
    try:
        df = pd.read_csv("data/collection_points.csv")
        for _, row in df.iterrows():
            color = {
                'hotel': 'blue',
                'kirana': 'purple',
                'cafe': 'orange',
                'bar': 'red'
            }.get(row['category'], 'gray')

            folium.Marker(
                location=[latitude, longitude],
                icon=folium.DivIcon(html=f"""
                <div style="width:10px; height:10px; background-color:{color};"></div>
                """)
            ).add_to(m)

    except Exception as e:
        print("Error loading markers:", e)

    # ---- 2. Add 1 km² Grid Overlay ----
    lat_min, lat_max = 14.9, 15.9
    lon_min, lon_max = 73.7, 74.3
    lat_step = 0.009
    lon_step = 0.009

    lat_vals = list(np.arange(lat_min, lat_max, lat_step))
    lon_vals = list(np.arange(lon_min, lon_max, lon_step))

    for lat in lat_vals:
        for lon in lon_vals:
            bounds = [
                [lat, lon],
                [lat + lat_step, lon],
                [lat + lat_step, lon + lon_step],
                [lat, lon + lon_step],
                [lat, lon]
            ]
            folium.PolyLine(bounds, color="white", weight=0.5, opacity=0.5).add_to(m)

    # ---- 3. Render map in Streamlit ----
    components.html(m._repr_html_(), height=600)
