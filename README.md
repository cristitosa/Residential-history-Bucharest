Residential History of Bucharest (1989-2017) 🗺️
This project provides an interactive visualization of the historical residential locations (houses vs. apartments) in the Bucharest metropolitan area from 1989 to 2017. The application is built using Python with Streamlit for the web interface and Folium for map rendering.

✨ Live Demo
You can explore the live application here: https://residential-history-bucharest.streamlit.app/

<img width="803" height="847" alt="image" src="https://github.com/user-attachments/assets/ff72965c-0ece-4f84-8b1c-745f86723788" />

Features
Interactive Map: Displays geographical data on a Folium map centered on Bucharest.

Time-Lapse Visualization: A slider allows users to select a year between 1989 and 2017 to see the residential landscape for that specific year.

Color-Coded Data:

<span style="color:green">Green</span> markers represent houses 🏡.

<span style="color:blue">Blue</span> markers represent apartments 🏢.

Dynamic Legend: A legend on the map updates to show the currently selected year.

Geographical Bounding: The data is filtered to display only points within the Bucharest metropolitan area.

💾 Data Sources
The visualization is generated from two primary data files:

TS_Coord_Res.csv: This file contains the time-series geographical data, with columns for each year's latitude (YYYY_lat) and longitude (YYYY_long) for each residential ID.

Baza_Life_Trajectory.xlsx: This Excel file contains the life trajectory data, mapping a response ID to a building type (1 for House, 2 for Apartment) for each year.

⚙️ Setup and Installation
To run this project locally, please follow these steps.

Prerequisites
Python 3.8+

Git

Installation Steps
Clone the repository:

Bash

git clone https://github.com/your-username/Residential-history-Bucharest.git
cd Residential-history-Bucharest
Create a virtual environment (recommended):

On macOS/Linux:

Bash

python3 -m venv venv
source venv/bin/activate
On Windows:

Bash

python -m venv venv
venv\Scripts\activate
Install the required dependencies:

Bash

pip install -r requirements.txt
(Note: You need to create the requirements.txt file. See the "Improvements" section below.)

🚀 Usage
Once the setup is complete, run the Streamlit application with the following command:

Bash

streamlit run app.py
(Assuming you have named your Python script app.py)

The application will open in a new tab in your default web browser.

💡 Code Breakdown
The main script performs the following actions:

Imports & Configuration: Loads necessary libraries (streamlit, pandas, folium) and sets up initial configurations like file paths and the Bucharest bounding box.

Data Loading: Reads the coordinate and trajectory data from the CSV and Excel files into pandas DataFrames.

generate_map(year) Function:

Takes a year as input.

Reshapes and filters both DataFrames to get a clean list of coordinates and building types for that specific year.

Merges the two data sources based on ID and year.

Filters the data to the specified geographical bounding box.

Creates a folium.Map centered on Bucharest.

Iterates through the filtered data, adding a folium.CircleMarker for each data point, colored according to its building type.

Injects a custom HTML legend onto the map to display the year and color key.

Streamlit UI:

Sets the application title using st.title().

Creates an interactive year-selection st.slider().

Calls the generate_map() function with the year selected by the user.

Renders the final map object using the st_folium() component.
