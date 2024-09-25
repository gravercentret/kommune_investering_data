import pandas as pd
import numpy as np

data_path = "../data/investeringer_datagrundlag.xlsx"
df = pd.read_excel(data_path)

### Cleaning df_kilde
# Replace '-' with NaN (remove entries with no value)
df["Markedsværdi (DKK)"] = df["Markedsværdi (DKK)"].replace("-", np.nan)

# Remove any non-numeric characters except for digits and decimal points
df["Markedsværdi (DKK)"] = df["Markedsværdi (DKK)"].replace(r"[^\d.]", "", regex=True)

# Convert the column to float (after cleaning)
df["Markedsværdi (DKK)"] = pd.to_numeric(df["Markedsværdi (DKK)"], errors="coerce")

df = df[df["Kommune"].notna()]
df = df[df["ISIN kode"].notna()]

df_kilde = df

### Merging with ISIN
# The 'red' list of companies on exclusion lists
isin_path = "../data/all_exclude_lists_isin.xlsx"
df_isin = pd.read_excel(isin_path)
df_isin["OBS_Type"] = "red"

# The 'orange' of countries on exclusion lists
isin_path_country = "../data/all_exclude_country_lists_isin.xlsx"
df_isin_c = pd.read_excel(isin_path_country)
df_isin_c["OBS_Type"] = "orange"
df_isin_c = df_isin_c.rename(columns={"Land": "Selskab"})

# Merging together
df_both_isin = pd.concat([df_isin, df_isin_c], ignore_index=True)
df_both_isin.drop("Land oversat", axis=1, inplace=True)

# The 'yellow' with our findings
yellow_path = "../data/Gule selskaber.xlsx"
df_yellow = pd.read_excel(yellow_path)
df_yellow["OBS_Type"] = "yellow"
df_yellow.rename(
    columns={
        "ISIN kode": "ISIN",
        "Årsag": "Årsag til eksklusion",
        "Værdipapirets navn": "Matched Værdipapirets navn",
        "Udsteder": "Selskab",
    },
    inplace=True,
)
df_yellow.drop("Type", axis=1, inplace=True)
df_yellow["Årsag til eksklusion"] = "Gravercentret: " + df_yellow["Årsag til eksklusion"].astype(
    str
)

df_all_lists = pd.concat([df_both_isin, df_yellow], ignore_index=True)

### Sort to keep only unique - Ordered by 'Red', 'Orange', 'Yellow:
# Assign a numeric ranking to the 'OBS_Type' column
priority_map = {"red": 3, "orange": 2, "yellow": 1}

# Add a new column 'Priority' to your dataframe to represent the priority of each OBS_Type
df_all_lists["Priority"] = df_all_lists["OBS_Type"].map(priority_map)

# Find duplicate ISINs
duplicate_isin = df_all_lists[df_all_lists.duplicated(subset="ISIN", keep=False)]

# Group duplicates by 'ISIN' and keep the row with the highest priority
df_deduplicated = duplicate_isin.loc[duplicate_isin.groupby("ISIN")["Priority"].idxmax()]

# If you want to update your original dataframe by removing duplicates and keeping the highest priority:
df_cleaned = df_all_lists.drop_duplicates(subset="ISIN", keep=False)  # Remove all duplicates first
df_final_isin_lists = pd.concat([df_cleaned, df_deduplicated], ignore_index=True)

### Merge with our original data
# Perform a left merge on the 'ISIN kode' from df_kilde and 'ISIN' from df_isin
merged_df = pd.merge(
    df_kilde, df_final_isin_lists, how="left", left_on="ISIN kode", right_on="ISIN"
)

# Save the merged DataFrame to a new Excel file if needed
merged_df.to_excel("../data/merged_data_exc_list_and_org.xlsx", index=False)
