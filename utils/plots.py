import pandas as pd
import polars as pl
import streamlit as st
import matplotlib.pyplot as plt

def create_pie_chart(filtered_df):
    # Group the data by 'Type' and sum the 'Markedsværdi (DKK)'
    type_distribution = (
        filtered_df.group_by("Type")
        .agg(pl.col("Markedsværdi (DKK)").sum().alias("Total Markedsværdi"))
        .to_pandas()
    )  # Convert to pandas for plotting

    # Drop rows with missing values (NaN) in 'Total Markedsværdi' or 'Type'
    type_distribution = type_distribution.dropna(subset=["Total Markedsværdi", "Type"])

    # Combine 'Andet' and 'Ikke angivet' into one category
    type_distribution["Type"] = type_distribution["Type"].replace(
        {"Andet": "Andet/Ikke angivet", "Ikke angivet": "Andet/Ikke angivet"}
    )

    # Re-aggregate the data to group by the combined category, summing only the numeric column
    type_distribution = type_distribution.groupby("Type", as_index=False)[
        "Total Markedsværdi"
    ].sum()

    # Define a color mapping for consistent colors
    color_mapping = {
        "Aktie": "cornflowerblue",
        "Obligation": "lightgreen",
        "Virksomhedsobligation": "lightblue",
        "Andet/Ikke angivet": "lightgray",
    }

    # Match the colors with the values in 'Type'
    colors = [color_mapping.get(type_val, "gray") for type_val in type_distribution["Type"]]

    # Plot the pie chart using matplotlib
    fig, ax = plt.subplots()
    ax.pie(
        type_distribution["Total Markedsværdi"],
        colors=colors,
        startangle=0,
        autopct="%1.1f%%",
        textprops={"fontsize": 14},
    )

    # Add a legend with the 'Type' values
    ax.legend(
        type_distribution["Type"], title="Type", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1)
    )

    # Display the pie chart in Streamlit
    st.pyplot(fig)
