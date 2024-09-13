import pandas as pd
import streamlit as st

def set_pandas_options():
    # Set all the pandas options here
    pd.set_option("styler.render.max_elements", 1127048)
    # Add more settings as needed

def set_streamlit_options():

    st.set_page_config(layout="wide")