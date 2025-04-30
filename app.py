import streamlit as st
from model import run_simulation
from map_utils import show_map

st.set_page_config(layout="wide")
st.title("Goa DRS Simulation Model")

st.sidebar.header("Simulation Inputs")
rvm_count = st.sidebar.slider("Number of RVMs", 10, 100, 25)
truck_capacity = st.sidebar.selectbox("Truck Capacity (kg)", [200, 500, 1000])
pickup_frequency = st.sidebar.selectbox("Pickup Frequency (in days)", [1, 2, 3])
simulate = st.sidebar.button("Run Simulation")

if simulate:
    results = run_simulation(rvm_count, truck_capacity, pickup_frequency)
    st.subheader("Simulation Output")
    st.metric("Total Bottles Collected", f"{results['bottles_collected']:,}")
    st.metric("Estimated Trips", results['trips_required'])

st.subheader("Map View")
show_map()
