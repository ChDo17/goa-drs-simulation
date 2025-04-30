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
