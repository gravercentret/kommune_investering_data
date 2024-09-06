import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from utils.data_prep import data_processing, data_split_kom_reg

# Load and process data
path = "data/data_investeringer.xlsx"
df = pd.read_excel(path)
df = data_processing(df)
df_reg, df_kom = data_split_kom_reg(df)

st.write("Region Data")

# Create a multiselect box for filtering "Kommune" values
selected_regions = st.multiselect(
    "Select Region Kommune(s):",
    df_reg["Kommune"].dropna().unique(),
    default=df_reg["Kommune"].dropna().unique(),
)

# Filter the dataframe based on selected regions
filtered_df_reg = df_reg[df_reg["Kommune"].isin(selected_regions)]

# Display basic information for the filtered data
total_rows_reg = filtered_df_reg.shape[0]
total_markedsværdi_reg = filtered_df_reg["Markedsværdi (DKK)"].sum()

st.write(f"Total rows: {total_rows_reg}")
st.write(f"Total Markedsværdi (DKK): {total_markedsværdi_reg:,.2f}")

# Display the filtered dataframe
st.write("Filtered Region Data:")
st.dataframe(filtered_df_reg)

# Layout the plots side by side
col1, col2 = st.columns(2)

with col1:
    st.write("Comparison of Selected Regions (Amount of Rows):")

    if not filtered_df_reg.empty:
        # Pivot the data to prepare for stacked bar plot (amount of rows)
        type_counts = filtered_df_reg.pivot_table(
            index='Kommune',
            columns='Type',
            aggfunc='size',
            fill_value=0
        )

        fig, ax = plt.subplots(figsize=(10, 6))

        # Plot a stacked bar chart (amount of rows)
        type_counts.plot(kind='bar', stacked=True, ax=ax)

        ax.set_xlabel("Kommune")
        ax.set_ylabel("Number of Entries")
        ax.set_title("Distribution of Types by Kommune (Amount of Rows)")
        ax.legend(title="Type")
        ax.tick_params(axis="x", rotation=45)

        # Display the plot
        st.pyplot(fig)
    else:
        st.write("No data available for the selected Region(s).")

with col2:
    st.write("Comparison of Selected Regions (Total Markedsværdi):")

    if not filtered_df_reg.empty:
        # Pivot the data to prepare for stacked bar plot (total Markedsværdi)
        type_sums = filtered_df_reg.pivot_table(
            index='Kommune',
            columns='Type',
            values='Markedsværdi (DKK)',
            aggfunc='sum',
            fill_value=0
        )

        fig, ax = plt.subplots(figsize=(10, 6))

        # Plot a stacked bar chart (total Markedsværdi)
        type_sums.plot(kind='bar', stacked=True, ax=ax)

        ax.set_xlabel("Kommune")
        ax.set_ylabel("Total Markedsværdi (DKK)")
        ax.set_title("Distribution of Total Markedsværdi by Kommune and Type")
        ax.legend(title="Type")
        ax.tick_params(axis="x", rotation=45)

        # Display the plot
        st.pyplot(fig)
    else:
        st.write("No data available for the selected Region(s).")
