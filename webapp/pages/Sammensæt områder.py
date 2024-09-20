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

df = st.session_state.df_pl

if "multiselect" not in st.session_state:
    st.session_state.multiselect = []

st.title("Sammenlign Kommuner")

options = st.multiselect(
    "What are your favorite colors",
    df["Kommune"].unique(),
)

filtered_df = df[[options]]

st.dataframe(filtered_df)
