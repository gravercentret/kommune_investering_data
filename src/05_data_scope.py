import pandas as pd

data_path = "merged_data.xlsx"
merged_df = pd.read_excel(data_path)

# List of relevant organizations
relevant_organizations = [
    "FN",
    "AP Pension",
    "Akademiker Pension" "ATP",
    "Lærernes Pension",
    "Nordea",
    "PensionDanmark",
    "PFA",
    "Sydinvest",
    "Velliv",
]


# Function to extract information from 'Årsag til eksklusion'
def extract_organisations(row):
    if pd.isna(row) or row.strip() == "":
        return "", ""

    # Split the column by semicolons
    parts = row.split(";")

    # Initialize variables
    fn_value = ""
    pension_companies = []

    # Loop through each part and extract relevant info
    for part in parts:
        part = part.strip()  # Strip leading/trailing spaces
        org_name = part.split(":")[0].strip()  # Extract organization name

        # If organization is in the relevant list
        if org_name in relevant_organizations:
            if org_name == "FN":
                fn_value = "FN"
            else:
                pension_companies.append(org_name)

    # Create values for new columns
    pension_value = "; ".join(pension_companies) if pension_companies else ""

    return fn_value, pension_value


# Apply the extraction function to the DataFrame and create new columns
merged_df[["Problematisk ifølge (FN)", "Problematisk ifølge (pensionsselskab)"]] = merged_df[
    "Årsag til eksklusion"
].apply(lambda row: pd.Series(extract_organisations(row)))

# Save the merged DataFrame to a new Excel file if needed
merged_df.to_excel("full_data.xlsx", index=False)

### Antal kommuner problematisk ifølge FN (58)
# len(merged_df[merged_df['Problematisk ifølge (FN)']=='FN']['Kommune'].unique())

### Der er 71 kommuner, hvor der er problematiske investeringer

### Der er 21 kommuner uden noget problematisk
# First, filter the rows where 'Årsag til eksklusion' is empty or NaN
# empty_arsag_df = merged_df[merged_df['Årsag til eksklusion'].isna() | (merged_df['Årsag til eksklusion'] == "")]

# # Now, find Kommuner that do not have any non-empty 'Årsag til eksklusion'
# # Get all unique Kommuner
# all_kommuner = merged_df['Kommune'].unique()

# # Get Kommuner that have non-empty 'Årsag til eksklusion'
# kommuner_with_arsag = merged_df[~merged_df['Årsag til eksklusion'].isna() & (merged_df['Årsag til eksklusion'] != "")]['Kommune'].unique()

# # Find Kommuner that do not have any non-empty 'Årsag til eksklusion'
# kommuner_without_arsag = set(all_kommuner) - set(kommuner_with_arsag)

# # Convert to a list or display it
# kommuner_without_arsag = list(kommuner_without_arsag)

# print(f"Kommune(s) with no rows with a value in 'Årsag til eksklusion': {kommuner_without_arsag}")
