import polars as pl
import plotly.express as px
import streamlit as st
from utils.data_prep import (
    round_to_million,
)


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
    type_distribution["color"] = type_distribution["Type"].map(color_mapping)

    # Apply rounding to 'Total Markedsværdi' for display in hover text
    type_distribution["Markedsværdi_display"] = type_distribution["Total Markedsværdi"].apply(
        round_to_million
    )

    # Create a pie chart using Plotly
    fig = px.pie(
        type_distribution,
        values="Total Markedsværdi",
        names="Type",
        color="Type",  # Set colors for categories
        color_discrete_map=color_mapping,
        title="Typer af fordel på økonomisk andel",
    )
    fig.update_traces(
        textinfo="percent",
        hovertemplate="<b>%{label}</b><br>Markedsværdi: %{customdata}<extra></extra>",
        customdata=type_distribution["Markedsværdi_display"],  # Use the rounded values in hover
        sort=False,  # Keeps the original order of the data
        rotation=90,
    )  # Rotates the pie chart

    # Adjust the layout to prevent text from being cut off
    fig.update_layout(
        title=dict(
            font=dict(size=20),
        ),
        showlegend=True,
        legend_title="Type",
        legend=dict(
            x=1,  # Adjusts horizontal position of the legend
            y=1,  # Adjusts vertical position of the legend
            traceorder="normal",
            font=dict(size=14),
            bgcolor="rgba(0,0,0,0)",  # Transparent background
        ),
        margin=dict(l=50, r=150, t=50, b=50),  # Increase right margin for legend
    )
    st.plotly_chart(fig)
