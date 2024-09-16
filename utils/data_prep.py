import numpy as np
from sqlalchemy import create_engine
import polars as pl

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
