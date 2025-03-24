import os
import time
import pandas as pd
import folium
import streamlit as st
from streamlit_folium import st_folium

# Define bounding box for Bucharest metro area
bounding_box = [(44.310548, 25.900933), (44.660081, 26.283315)]  # [(min_lat, min_long), (max_lat, max_long)]

# File paths (ensure correct paths when deploying)
coord_file_path = "TS_Coord_Res.csv"
trajectory_file_path = "Baza_Life_Trajectory.xlsx"

# Load data
@st.cache_data
def load_data():
    coordinates_df = pd.read_csv(coord_file_path)
    trajectory_df = pd.read_excel(trajectory_file_path, sheet_name="Sheet3")
    return coordinates_df, trajectory_df

coordinates_df, trajectory_df = load_data()

# Streamlit UI
st.title("🏙️ Bucharest Housing Animation")
st.sidebar.header("Select Year")

# Select year slider
selected_year = st.sidebar.slider("Choose a Year", min_value=1989, max_value=2017, step=1, value=2000)

# Function to generate the map
def generate_map(year):
    coord_list = []
    for index, row in coordinates_df.iterrows():
        id_val = row.iloc[0]  # Assuming first column is ID
        lat_col, long_col = f"{year}_lat", f"{year}_long"
        if lat_col in row and long_col in row:
            coord_list.append({'ID': id_val, 'Year': year, 'Latitude': row[lat_col], 'Longitude': row[long_col]})

    coordinates_long = pd.DataFrame(coord_list)

    # Convert trajectory_df to long format
    trajectory_long = pd.melt(trajectory_df, id_vars=['Response ID'], var_name='Year', value_name='Building Type')
    trajectory_long.rename(columns={'Response ID': 'ID'}, inplace=True)
    trajectory_long['Year'] = pd.to_numeric(trajectory_long['Year'], errors='coerce').dropna().astype(int)
    trajectory_long['Building Type'] = pd.to_numeric(trajectory_long['Building Type'], errors='coerce').fillna(0).astype(int)

    # Merge data
    merged_data = pd.merge(coordinates_long, trajectory_long, on=['ID', 'Year'], how='inner')
    merged_data = merged_data.dropna(subset=['Latitude', 'Longitude'])
    merged_data = merged_data[merged_data['Building Type'].isin([1, 2])]

    # Apply bounding box
    merged_data = merged_data[
        (merged_data['Longitude'] >= bounding_box[0][1]) & (merged_data['Longitude'] <= bounding_box[1][1]) &
        (merged_data['Latitude'] >= bounding_box[0][0]) & (merged_data['Latitude'] <= bounding_box[1][0])
    ]

    # Create map centered on Bucharest
    map_year = folium.Map(location=[(bounding_box[0][0] + bounding_box[1][0]) / 2,
                                    (bounding_box[0][1] + bounding_box[1][1]) / 2],
                          zoom_start=12)
    map_year.fit_bounds(bounding_box)

    # Add markers
    for _, row in merged_data.iterrows():
        color = 'green' if row['Building Type'] == 1 else 'blue'
        folium.CircleMarker(
            location=[row['Latitude'], row['Longitude']],
            radius=2,
            color=color,
            fill=True,
            fill_color=color,
            fill_opacity=0.7,
            tooltip=f"ID: {row['ID']}, Year: {row['Year']}, Type: {row['Building Type']}"
        ).add_to(map_year)

    return map_year

# Generate and display map
st_folium(generate_map(selected_year), width=700, height=500)
