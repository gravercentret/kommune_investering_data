import numpy as np
from sqlalchemy import create_engine
import polars as pl
import streamlit as st

# Create an SQLite engine


def get_data():
    engine = create_engine("sqlite:///src/investerings_database.db")

    query = """
        SELECT [Kommune], [ISIN kode], [Værdipapirets navn], 
        [Udsteder], [Markedsværdi (DKK)], [Type], 
        [Problematisk ifølge:], 
        [Årsag til eksklusion]
        FROM kommunale_regioner_investeringer;
    """

    # Execute the query and load the result into a Polars DataFrame
    with engine.connect() as conn:
        df_polars = pl.read_database(query, conn)

    return df_polars

def get_unique_kommuner(df_pl):
    """
    Extract unique 'Kommune' values from the dataframe and sort them alphabetically.
    """
    return sorted(df_pl["Kommune"].unique().to_list())


def filter_dataframe_by_choice(df_pl, choice, all_values="Hele landet", municipalities="Alle kommuner", regions="Alle regioner"):
    """
    Filter the dataframe based on the user's selection (all_values, municipalities, regions, or a specific kommune).
    """
    if choice == all_values:
        return df_pl
    elif choice == municipalities:
        return df_pl.filter(~df_pl["Kommune"].str.starts_with("Region"))
    elif choice == regions:
        return df_pl.filter(df_pl["Kommune"].str.starts_with("Region"))
    else:
        return df_pl.filter(df_pl["Kommune"] == choice)

import pandas as pd

def filter_df_by_search(df, search_query):
    # Use case-insensitive search if query is provided
    if search_query:
        # Create a case-insensitive regex search pattern
        search_pattern = f"(?i){search_query}"

        # Replace NA values with empty strings and cast columns to string
        df = df.with_columns([pl.col(col).fill_null("").cast(str) for col in df.columns])

        # Combine conditions across all columns using logical OR (|) operator
        filter_expr = None
        for col in df.columns:
            condition = pl.col(col).str.contains(search_pattern)
            filter_expr = condition if filter_expr is None else filter_expr | condition

        # Apply the filter
        filtered_df = df.filter(filter_expr)
    else:
        filtered_df = df
    return filtered_df

def fix_column_types(df):
    # Cast 'Markedsværdi (DKK)' back to float
    df = df.with_columns([
        pl.col("Markedsværdi (DKK)").cast(pl.Float64)
    ])
    return df

# Function to generate a single line with links
def generate_organization_links(df, column_name):
    org_links = {
        "FN": 'https://www.un.org/',
        "AP Pension": 'https://www.appension.dk/',
        "Akademiker Pension": 'https://www.ap.dk/',
        "ATP": 'https://www.atp.dk/',
        "Lærernes Pension": 'https://www.lpension.dk/',
        "Nordea": 'https://www.nordea.dk/',
        "PensionDanmark": 'https://www.pensiondanmark.dk/',
        "PFA": 'https://www.pfa.dk/',
        "Sydinvest": 'https://www.sydinvest.dk/',
        "Velliv": 'https://www.velliv.dk/',
    }
    # Extract all unique organizations from the dataframe column
    unique_orgs = set()
    
    for org_list in df[column_name]:
        if org_list is not None:
            orgs = org_list.split("; ")
            for org in orgs:
                unique_orgs.add(org.strip())
    
    # Generate the links as one line
    links = "; ".join([f"[{org}]({org_links[org]})" for org in unique_orgs if org in org_links])
    
    # Display the bold title and links
    st.markdown(f"**Links til relevante eksklusionslister:** {links}")


# def data_processing(df):
#     # Removing columns with no muncipality
#     df = df[df["Kommune"].notna()]

#     # Replace '-' with NaN (Fjerner dem, hvor der ikke er værdi. Det er fx to fra Odense)
#     df["Markedsværdi (DKK)"] = df["Markedsværdi (DKK)"].replace("-", np.nan)

#     # Remove any potential commas, spaces, or other non-numeric characters
#     df["Markedsværdi (DKK)"] = df["Markedsværdi (DKK)"].replace({",": "", " ": ""}, regex=True)

#     # Convert the column to float
#     df["Markedsværdi (DKK)"] = df["Markedsværdi (DKK)"].astype(float)

#     # Sort the dataframe alphabetically by "Kommune" in a case-insensitive manner
#     df = df.sort_values(by=["Kommune", "Markedsværdi (DKK)"], ascending=[True, False])

#     df["Kommune"] = df["Kommune"].str.strip()
#     return df


# def data_split_kom_reg(df):
#     # Filter rows where "Kommune" starts with "Region"
#     df_reg = df[df["Kommune"].str.startswith("Region")]

#     # Filter all other rows
#     df_kom = df[~df["Kommune"].str.startswith("Region")]
#     return df_reg, df_kom
