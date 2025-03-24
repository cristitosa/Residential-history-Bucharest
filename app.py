import os
import time
import folium
import pandas as pd
import streamlit as st
from streamlit_folium import st_folium
from folium.plugins import FloatImage

# Define file paths
coord_file_path = "TS_Coord_Res.csv"
trajectory_file_path = "Baza_Life_Trajectory.xlsx"

# Define bounding box for Bucharest metro area
bounding_box = [(44.310548, 25.900933), (44.660081, 26.283315)]  # [(min_lat, min_long), (max_lat, max_long)]

# Years for animation
years_to_animate = list(range(1989, 2018))

# Load data
coordinates_df = pd.read_csv(coord_file_path)
trajectory_df = pd.read_excel(trajectory_file_path, sheet_name="Sheet3")


# Function to generate the map
def generate_map(year):
    # Filter and process the data
    coord_list = []
    for index, row in coordinates_df.iterrows():
        id_val = row.iloc[0]  # Assuming first column is ID
        lat_col = f"{year}_lat"
        long_col = f"{year}_long"
        if lat_col in row and long_col in row:
            coord_list.append({'ID': id_val, 'Year': year, 'Latitude': row[lat_col], 'Longitude': row[long_col]})

    coordinates_long = pd.DataFrame(coord_list)

    # Convert trajectory_df to long format
    trajectory_long = pd.melt(trajectory_df, id_vars=['Response ID'], var_name='Year', value_name='Building Type')
    trajectory_long.rename(columns={'Response ID': 'ID'}, inplace=True)
    trajectory_long['Year'] = pd.to_numeric(trajectory_long['Year'], errors='coerce').dropna().astype(int)
    trajectory_long['Building Type'] = pd.to_numeric(trajectory_long['Building Type'], errors='coerce').fillna(0).astype(int)

    # Merge dataframes
    merged_data = pd.merge(coordinates_long, trajectory_long, on=['ID', 'Year'], how='inner')
    merged_data = merged_data.dropna(subset=['Latitude', 'Longitude'])
    merged_data = merged_data[merged_data['Building Type'].isin([1, 2])]

    # Apply bounding box filter
    merged_data = merged_data[
        (merged_data['Longitude'] >= bounding_box[0][1]) & (merged_data['Longitude'] <= bounding_box[1][1]) &
        (merged_data['Latitude'] >= bounding_box[0][0]) & (merged_data['Latitude'] <= bounding_box[1][0])
    ]

    # Create the Folium map centered on Bucharest
    map_year = folium.Map(location=[(bounding_box[0][0] + bounding_box[1][0]) / 2,
                                    (bounding_box[0][1] + bounding_box[1][1]) / 2],
                          zoom_start=12)

    # Ensure correct zoom using fit_bounds
    map_year.fit_bounds(bounding_box)

    # Add markers
    for _, row in merged_data.iterrows():
        color = 'green' if row['Building Type'] == 1 else 'blue'
        folium.CircleMarker(
            location=[row['Latitude'], row['Longitude']],
            radius=3,  # Increased for better visibility
            color=color,
            fill=True,
            fill_color=color,
            fill_opacity=0.7,
            tooltip=f"ID: {row['ID']}, Year: {row['Year']}, Type: {row['Building Type']}"
        ).add_to(map_year)

    # Add a title and legend using HTML/CSS
    legend_html = '''
    <div style="position: fixed; bottom: 50px; left: 50px; width: 200px; height: 90px;
                background-color: white; z-index:9999; font-size:14px; border-radius:10px;
                padding: 10px; box-shadow: 2px 2px 6px rgba(0,0,0,0.3);">
    <b>Legend - Year {}</b><br>
    <i style="background:green; width: 12px; height: 12px; display: inline-block; border-radius: 50%;"></i> House 🏡<br>
    <i style="background:blue; width: 12px; height: 12px; display: inline-block; border-radius: 50%;"></i> Apartment 🏢
    </div>
    '''.format(year)

    map_year.get_root().html.add_child(folium.Element(legend_html))

    return map_year


# Streamlit App
st.title("Residential History of Bucharest")

# Add a slider for the year selection
year = st.slider("Select Year", min_value=1989, max_value=2017, value=2000)

# Generate and display the map
map_object = generate_map(year)
st_folium(map_object, width=800, height=600)
