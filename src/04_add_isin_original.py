import pandas as pd
import numpy as np

data_path = "../data/investeringer_datagrundlag.xlsx"
df = pd.read_excel(data_path)

### Obs - Nyt data for KBH
# Step 2: Remove rows where 'Kommune' is 'København'
df_filtered = df[df['Kommune'] != 'København']

# Step 3: Load the new data from 'Københavns Kommune-august2024.xlsx'
new_data_path = "../data/Københavns Kommune-august2024.xlsx"
df_new = pd.read_excel(new_data_path)

# Step 4: Append the new data to the filtered dataframe
df_concat = pd.concat([df_filtered, df_new], ignore_index=True)


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
df_yellow["ISIN kode"] = df_yellow["ISIN kode"].str.strip()
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
df_yellow["Eksklusionsårsager"] = df_yellow["Årsag til eksklusion"]
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

# Filter out the duplicates that have 'yellow' in OBS_Type (remove all 'yellow' duplicates)
# duplicate_isin = duplicate_isin[duplicate_isin["OBS_Type"] != "yellow"]

# duplicate_isin = duplicate_isin[duplicate_isin.duplicated(subset="ISIN", keep=False)]


def merge_reason(group):
    # Sort the group by priority (red first, then orange)
    group = group.sort_values(by="Priority", ascending=True)

    # Remove the yellow
    group = group[group["OBS_Type"] != "yellow"]
    # Concatenate 'Årsag til eksklusion' from the rows, using ';' as separator
    try:
        merged_reason = "; ".join(group["Årsag til eksklusion"])

        # Split the merged reason by ';' and remove duplicates
        unique_reasons = list(set(merged_reason.split("; ")))
        # Sort the unique reasons to maintain order and join them back together
        merged_cleaned_reason = "; ".join(unique_reasons)

        # Assign the cleaned, merged reason to the highest-priority row (first one after sorting)
        group["Årsag til eksklusion"] = merged_cleaned_reason

        ## Ny kode - Eksklusionsårsager
        merged_reason_2 = "; ".join(group["Eksklusionsårsager"])

        # Split the merged reason by ';' and remove duplicates
        unique_reasons_2 = list(set(merged_reason_2.split("; ")))
        # Sort the unique reasons to maintain order and join them back together
        merged_cleaned_reason_2 = "; ".join(unique_reasons_2)

        # Assign the cleaned, merged reason to the highest-priority row (first one after sorting)
        group["Eksklusionsårsager"] = merged_cleaned_reason_2
    except:
        pass
    # Keep the row with the highest priority (red over orange)
    return group.iloc[0].copy()  # Return a copy to avoid view-related issues


# Apply the merge function to the duplicate ISINs
df_deduplicated = duplicate_isin.groupby("ISIN").apply(merge_reason)

# Optionally, reset the index if needed
df_deduplicated = df_deduplicated.reset_index(drop=True)

# If you want to update your original dataframe by removing duplicates and keeping the highest priority:
df_cleaned = df_all_lists.drop_duplicates(subset="ISIN", keep=False)
df_final_isin_lists = pd.concat([df_cleaned, df_deduplicated], ignore_index=True)

### Merge with our original data
# Perform a left merge on the 'ISIN kode' from df_kilde and 'ISIN' from df_isin
merged_df = pd.merge(
    df_kilde, df_final_isin_lists, how="left", left_on="ISIN kode", right_on="ISIN"
)

# Save the merged DataFrame to a new Excel file if needed
merged_df.to_excel("../data/merged_data_exc_list_and_org.xlsx", index=False)
