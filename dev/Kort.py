# import streamlit as st
# import geopandas as gpd
# import pandas as pd
# import folium
# from streamlit_folium import st_folium

# # Load your data and GeoJSON
# from utils.data_prep import data_processing, data_split_kom_reg

# # Load and process data
# path = "data/data_investeringer.xlsx"
# df = pd.read_excel(path)
# df = data_processing(df)
# df_reg, df_kom = data_split_kom_reg(df)

# # Load the GeoJSON file
# geojson_path = "data/municipalities.geojson"
# gdf = gpd.read_file(geojson_path)

# # Prepare the GeoDataFrame by merging it with your data
# gdf['Kommune'] = gdf['label_dk'].str.strip()

# # Simplify the geometries to reduce complexity
# gdf['geometry'] = gdf['geometry'].simplify(tolerance=0.001, preserve_topology=True)

# # Strip leading and trailing whitespace in both datasets before merging
# df_kom['Kommune'] = df_kom['Kommune'].str.strip()
# gdf['Kommune'] = gdf['Kommune'].str.strip()

# # Perform merge operation efficiently
# merged = gdf.merge(df_kom[['Kommune']], on='Kommune', how='left', indicator=True)

# # Add a new column to indicate whether the municipality is in your dataframe
# merged['In Dataframe'] = merged['_merge'] == 'both'

# # Create a folium map centered around Denmark
# m = folium.Map(location=[56.26392, 9.501785], zoom_start=7)

# folium.GeoJson(
#     merged[['geometry', 'Kommune']],
#     style_function=lambda feature: {
#         'fillColor': '#00FF00' if feature['properties']['Kommune'] in df_kom['Kommune'].values else '#FF0000',
#         'color': 'black',
#         'weight': 0.5,
#         'fillOpacity': 0.7,
#     },
#     tooltip=folium.GeoJsonTooltip(fields=["Kommune"]),
# ).add_to(m)

# # Add tooltips
# folium.GeoJsonTooltip(fields=["Kommune"]).add_to(m)

# # Create a new page in Streamlit
# st.title("Map of Danish Municipalities")

# st.write("This map highlights the municipalities that are present in the dataframe.")

# # Display the map in Streamlit
# st_folium(m, width=700, height=500)
