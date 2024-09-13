import streamlit as st
import pandas as pd
import polars as pl
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
from utils.data_prep import get_data, get_unique_kommuner, filter_dataframe_by_choice
from utils.styling import color_rows
from src.config import set_pandas_options, set_streamlit_options

# Apply the settings
set_pandas_options()
set_streamlit_options()

if "df_pl" not in st.session_state:
    st.session_state.df_pl = get_data()

# Title of the app
st.title("Investeringer")

# Get unique municipalities and sort alphabetically
unique_kommuner = get_unique_kommuner(st.session_state.df_pl)

# Define custom categories
all_values = "Hele landet"
municipalities = "Kommuner"
regions = "Regioner"

# Create dropdown options
dropdown_options = [all_values, municipalities, regions] + unique_kommuner

# Sidebar with selection options
with st.sidebar:
    user_choice = st.selectbox("Vælg område:", dropdown_options)

    st.header("Sådan gjorde vi")
    st.markdown(
        """
        Her kan vi have et kort metodeafsnit, og linke til mere.
        """
    )

# Filter dataframe based on user's selection
filtered_df = filter_dataframe_by_choice(st.session_state.df_pl, user_choice)

# Add a new column to mark problematic rows (rows with non-empty 'Problematisk ifølge:')
# filtered_df = filtered_df.with_columns(
#     (filtered_df["Problematisk ifølge:"].is_not_null()).alias("is_problematic")
# )

# Sort first by 'is_problematic' (so that True comes first), then by 'Kommune' and 'ISIN kode' alphabetically
# sorted_df = filtered_df.sort(["Problematisk ifølge:", "Kommune", "ISIN kode"], nulls_last=True)


# Convert to Pandas for displaying in Streamlit
filtered_df_pandas = filtered_df.to_pandas()

# Apply the color_rows function to highlight rows where 'Problematisk ifølge:' is not empty
# filtered_df_pandas = filtered_df_pandas.style.apply(color_rows, axis=1)

# Display the filtered dataframe
st.write(f'Data for "{user_choice}":')
st.dataframe(filtered_df_pandas)

