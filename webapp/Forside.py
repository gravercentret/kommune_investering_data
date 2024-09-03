import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def data_processing(df):
    # Removing columns with no muncipality
    df = df[df["Kommune"].notna()]

    # Replace '-' with NaN (Fjerner dem, hvor der ikke er værdi. Det er fx to fra Odense)
    df["Markedsværdi (DKK)"] = df["Markedsværdi (DKK)"].replace("-", np.nan)

    # Remove any potential commas, spaces, or other non-numeric characters
    df["Markedsværdi (DKK)"] = df["Markedsværdi (DKK)"].replace(
        {",": "", " ": ""}, regex=True
    )

    # Convert the column to float
    df["Markedsværdi (DKK)"] = df["Markedsværdi (DKK)"].astype(float)

    # Sort the dataframe alphabetically by "Kommune" in a case-insensitive manner
    df = df.sort_values(by=['Kommune', 'Markedsværdi (DKK)'], ascending=[True, False])
    return df


def data_split_kom_reg(df):
    # Filter rows where "Kommune" starts with "Region"
    df_reg = df[df["Kommune"].str.startswith("Region")]

    # Filter all other rows
    df_kom = df[~df["Kommune"].str.startswith("Region")]
    return df_reg, df_kom


path = "data/data_investeringer.xlsx"
df = pd.read_excel(path)
df = data_processing(df)
df_reg, df_kom = data_split_kom_reg(df)

# Streamlit App
# Set the page layout to wide
st.set_page_config(layout="wide")

# Title of the app
st.title("Filter Data by Kommune and Visualize")

# Create a dropdown in the sidebar for selecting a "Kommune" value
selected_kommune = st.sidebar.selectbox("Select a Kommune:", df['Kommune'].dropna().unique())

# Create two columns in the layout
df_col, plot_col = st.columns([3, 2])

with df_col:
    # Filter the dataframe based on the selected "Kommune"
    filtered_df_kom = df[df['Kommune'] == selected_kommune]

    # Display the filtered dataframe
    st.write("Kommune data:")
    st.dataframe(filtered_df_kom)

    # Display basic information
    total_rows = filtered_df_kom.shape[0]
    total_markedsværdi = filtered_df_kom['Markedsværdi (DKK)'].sum()

    st.write(f"Total rows: {total_rows}")
    st.write(f"Total Markedsværdi (DKK): {total_markedsværdi:,.2f}")


with plot_col:
    st.write("Type Distribution Plot:")
    
    # Distribution plot of "Type" column
    if not filtered_df_kom.empty:
        type_counts = filtered_df_kom['Type'].value_counts()
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.bar(type_counts.index, type_counts.values)
        ax.set_xlabel('Type')
        ax.set_ylabel('Count')
        ax.set_title(f'Distribution of Types for {selected_kommune}')
        
        # Display the plot
        st.pyplot(fig)
    else:
        st.write("No data available for this Kommune.")