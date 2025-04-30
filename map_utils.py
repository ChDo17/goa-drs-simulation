import folium
import streamlit.components.v1 as components

def show_map():
    m = folium.Map(
        location=[15.5, 73.8], 
        zoom_start=11,
        tiles="CartoDB dark_matter"
    )
    folium.Marker([15.4952, 73.8261], popup="Sample RVM", icon=folium.Icon(color="blue")).add_to(m)
    folium.Marker([15.5200, 73.8400], popup="MRF Center", icon=folium.Icon(color="green")).add_to(m)
    
    import streamlit.components.v1 as components
    components.html(m._repr_html_(), height=500)
