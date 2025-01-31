import os
import pandas as pd
import ast
import numpy as np

# Define the folder where your files are located
folder_path = "../data/Eksklusion_lande/"

# Step 1: Identify files ending with _isin.xlsx
isin_files = [
    file for file in os.listdir(folder_path) if file.endswith("_isin.xlsx")
]  # and file.startswith("FN")]

# Initialize an empty list to store dataframes
dataframes = []


# Function to safely evaluate ISIN list
def safe_eval_isin(isin_string):
    try:
        return ast.literal_eval(isin_string)  # Safely convert string to list
    except (ValueError, SyntaxError):
        return []  # Return empty list if conversion fails


# Step 2: Read each relevant file into a DataFrame
for file in isin_files:
    file_path = os.path.join(folder_path, file)

    # Extract the first part of the filename before the underscore '_'
    file_prefix = file.split("_")[0]
    print(file_prefix)

    df = pd.read_excel(file_path)

    # Select only the required columns
    df = df[
        [
            "Land",
            "Årsag til eksklusion",
            "Land oversat",
            "ISIN",
            "Matched Udsteder",
            "Matched Værdipapirets navn",
            "Kommuner",
        ]
    ]

    # Step 3: Modify 'Årsag til eksklusion' by adding the file prefix at the beginning
    df["Årsag til eksklusion"] = df["Årsag til eksklusion"].apply(lambda x: f"{file_prefix}: {x}")

    # Step 4: Filter rows where ISIN is not empty and safely explode the ISIN list into separate rows
    df["ISIN"] = df["ISIN"].apply(safe_eval_isin)  # Safely convert ISIN string to list
    df = df[df["ISIN"].apply(lambda x: len(x) > 0)]  # Filter rows where ISIN list is not empty
    df = df.explode("ISIN")  # Create a new row for each ISIN

    # Ensure ISIN is a string (since it may still be a list element after explode)
    df["ISIN"] = df["ISIN"].astype(str)

    # Step 5: Append the cleaned DataFrame to the list
    dataframes.append(df)

# Step 6: Concatenate all dataframes
final_df = pd.concat(dataframes, ignore_index=True)

# Save the final dataframe to a new Excel file if needed
final_df.to_excel("../data/filtered_lande_isin_data_with_prefix.xlsx", index=False)

final_df["Land"] = final_df["Land"].str.strip()


# Step 7: Collapse rows with the same ISIN
# Function to merge differing values into a semicolon-separated string
def merge_values(series):
    unique_vals = series.dropna().unique()
    if len(unique_vals) == 1:
        return unique_vals[0]  # If only one unique value, return it
    else:
        return "; ".join(map(str, unique_vals))  # If multiple values, join them with a semicolon


### Ændret fra ISIN til Land
# Perform the aggregation by Land
collapsed_df = (
    final_df.groupby("ISIN")
    .agg(
        {
            "Land": merge_values,
            # "ISIN": merge_values,
            "Matched Udsteder": merge_values,
            "Matched Værdipapirets navn": merge_values,
            "Årsag til eksklusion": merge_values,
            "Kommuner": merge_values,  # Assuming this is the column that contains lists
        }
    )
    .reset_index()
)

collapsed_df.to_excel("../data/unique_lande_all_isin.xlsx", index=False)


# Step 8: Flatten lists, deduplicate values, and return as a semicolon-separated string
def flatten_and_unique(val):
    all_values = []

    try:
        # If the value is a string containing semicolon-separated lists
        if isinstance(val, str):
            # Split by semicolon if the string contains multiple list representations
            parts = val.split(";")
            for part in parts:
                part = part.strip()
                # Try to convert each part to a list if it's a string representation of a list
                if part.startswith("[") and part.endswith("]"):
                    list_part = ast.literal_eval(part)
                    all_values.extend(list_part)  # Flatten the list into the overall collection
                else:
                    all_values.append(part)  # Append non-list items directly
        elif isinstance(val, list):
            all_values.extend(val)  # If it's already a list, just extend it to the collection
        else:
            all_values.append(val)  # If it's a single value, add it directly

        # Deduplicate and sort the values
        unique_vals = sorted(set([str(item).strip() for item in all_values if item]))
        return "; ".join(unique_vals)  # Return the values as a semicolon-separated string

    except (ValueError, SyntaxError):
        return val  # In case of an error, return the value as-is


# Apply the function to the columns that might contain lists stored as strings
collapsed_df["Kommuner"] = collapsed_df["Kommuner"].apply(flatten_and_unique)
collapsed_df["Matched Udsteder"] = collapsed_df["Matched Udsteder"].apply(flatten_and_unique)
collapsed_df["Matched Værdipapirets navn"] = collapsed_df["Matched Værdipapirets navn"].apply(
    flatten_and_unique
)

# # Save the collapsed dataframe to a new Excel file
# collapsed_df.to_excel("../data/all_exclude_isin_country.xlsx", index=False)

# # # Print the resulting DataFrame
# # print(collapsed_df)

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


# The 'orange' of countries on exclusion lists
# df_isin_c = collapsed_df
# df_isin_c['OBS_Type'] = 'orange'
# df_isin_c = df_isin_c.rename(columns={"Land": "Selskab"})

### Merge with our original data
# Perform a left merge on the 'ISIN kode' from df_kilde and 'ISIN' from df_isin
merged_df = pd.merge(df_kilde, collapsed_df, how="right", left_on="ISIN kode", right_on="ISIN")

# Save the merged DataFrame to a new Excel file if needed
merged_df.to_excel("../data/all_exclude_isin_country_merged_original.xlsx", index=False)
