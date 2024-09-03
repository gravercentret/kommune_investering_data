import numpy as np


def data_processing(df):
    # Removing columns with no muncipality
    df = df[df["Kommune"].notna()]

    # Replace '-' with NaN (Fjerner dem, hvor der ikke er værdi. Det er fx to fra Odense)
    df["Markedsværdi (DKK)"] = df["Markedsværdi (DKK)"].replace("-", np.nan)

    # Remove any potential commas, spaces, or other non-numeric characters
    df["Markedsværdi (DKK)"] = df["Markedsværdi (DKK)"].replace({",": "", " ": ""}, regex=True)

    # Convert the column to float
    df["Markedsværdi (DKK)"] = df["Markedsværdi (DKK)"].astype(float)

    # Sort the dataframe alphabetically by "Kommune" in a case-insensitive manner
    df = df.sort_values(by=["Kommune", "Markedsværdi (DKK)"], ascending=[True, False])

    df['Kommune'] = df['Kommune'].str.strip()
    return df


def data_split_kom_reg(df):
    # Filter rows where "Kommune" starts with "Region"
    df_reg = df[df["Kommune"].str.startswith("Region")]

    # Filter all other rows
    df_kom = df[~df["Kommune"].str.startswith("Region")]
    return df_reg, df_kom
