import folium
import pandas as pd
import streamlit.components.v1 as components

def show_map():
    m = folium.Map(location=[15.5, 73.8], zoom_start=10, tiles="CartoDB dark_matter")

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
                location=[row['latitude'], row['longitude']],
                popup=f"{row['name']} ({row['category']})",
                icon=folium.Icon(color=color)
            ).add_to(m)
    except Exception as e:
        print("Error loading markers:", e)

    components.html(m._repr_html_(), height=600)

        # Add 1km² grid overlay
    lat_min, lat_max = 14.9, 15.9
    lon_min, lon_max = 73.7, 74.3
    lat_step = 0.009  # approx 1 km
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
            folium.PolyLine(bounds, color="green", weight=0.5, opacity=0.5).add_to(m)

