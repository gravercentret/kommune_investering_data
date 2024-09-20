import streamlit as st
import pandas as pd
import polars as pl
import numpy as np
import re
from io import BytesIO
import matplotlib.pyplot as plt
from utils.data_prep import (
    get_data,
    get_unique_kommuner,
    filter_dataframe_by_choice,
    generate_organization_links,
    filter_df_by_search,
    fix_column_types,
)
from utils.styling import color_rows_limited
from src.config import set_pandas_options, set_streamlit_options

# Apply the settings
set_pandas_options()
set_streamlit_options()

# if "df_pl" not in st.session_state:
#     st.session_state.df_pl = get_data()

df = st.session_state.df_pl

st.title("Sammenlign Kommuner")

# Multiselect for choosing municipalities
if 'selected_kommuner' not in st.session_state:
    st.session_state.selected_kommuner = []

selected_kommuner = st.multiselect(
    'Vælg kommuner, du vil sammenligne:',
    df['Kommune'].unique(),
    default=st.session_state.selected_kommuner
)

# Update session state after selection
st.session_state.selected_kommuner = selected_kommuner

# Filter dataframe
if selected_kommuner:
    filtered_df = df[df['Kommune'].isin(selected_kommuner)]
    st.write(f"Viser resultater for: {', '.join(selected_kommuner)}")
    st.dataframe(filtered_df)
else:
    st.write("Vælg venligst en eller flere kommuner for at se data.")