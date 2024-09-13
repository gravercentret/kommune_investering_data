import pandas as pd

data_path = "..\data\merged_data_exc_list_and_org.xlsx"
merged_df = pd.read_excel(data_path)

merged_df["Kommune"] = merged_df["Kommune"].str.replace("\xa0", " ", regex=False)


# List of relevant organizations
relevant_organizations = [
    "FN",
    "AP Pension",
    "Akademiker Pension",
    "ATP",
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
                pension_companies.append(org_name)  # Include FN in 'Problematisk ifølge'
            else:
                pension_companies.append(org_name)

    # Create values for new columns
    pension_value = "; ".join(pension_companies) if pension_companies else ""

    return fn_value, pension_value


# Apply the extraction function to the DataFrame and create new columns
merged_df[["Problematisk ifølge FN", "Problematisk ifølge:"]] = merged_df[
    "Årsag til eksklusion"
].apply(lambda row: pd.Series(extract_organisations(row)))


### Fixing type
# Create the function to fill missing 'Type' based on the majority for each 'ISIN kode'
def fill_missing_type(df, min_rows=5, agree_threshold=0.8):
    def fill_type_for_group(group):
        # Count the missing values in 'Type' for this group
        missing_count = group["Type"].isna().sum()
        # print(f"ISIN kode: {group.name}, Missing 'Type' values: {missing_count}")

        # Get the count of each type in the group, excluding missing values
        type_counts = group["Type"].value_counts()

        # If there are no valid types in the group, skip this group
        if type_counts.empty:
            return group

        total_rows = len(group)
        most_common_type, most_common_count = type_counts.idxmax(), type_counts.max()

        # Check the condition: at least min_rows, and agreement should meet the threshold
        if total_rows >= min_rows and most_common_count / total_rows >= agree_threshold:
            # If conditions met, fill missing 'Type' with the most common type
            group["Type"] = group["Type"].fillna(most_common_type)

        return group

    # Group by 'ISIN kode' and apply the function to each group
    df = df.groupby("ISIN kode").apply(fill_type_for_group)

    return df


# Apply the function to fill missing 'Type' values
filled_df = fill_missing_type(merged_df, min_rows=5, agree_threshold=0.80)

# Save the merged DataFrame to a new Excel file if needed
filled_df.to_excel("../data/full_data.xlsx", index=False)


### Antal kommuner problematisk ifølge FN (58)
# len(filled_df[filled_df['Problematisk ifølge (FN)']=='FN']['Kommune'].unique())

### Der er 71 kommuner, hvor der er problematiske investeringer

### Der er 21 kommuner uden noget problematisk
# First, filter the rows where 'Årsag til eksklusion' is empty or NaN
# empty_arsag_df = filled_df[filled_df['Årsag til eksklusion'].isna() | (filled_df['Årsag til eksklusion'] == "")]

# # Now, find Kommuner that do not have any non-empty 'Årsag til eksklusion'
# # Get all unique Kommuner
# all_kommuner = filled_df['Kommune'].unique()

# # Get Kommuner that have non-empty 'Årsag til eksklusion'
# kommuner_with_arsag = filled_df[~filled_df['Årsag til eksklusion'].isna() & (filled_df['Årsag til eksklusion'] != "")]['Kommune'].unique()

# # Find Kommuner that do not have any non-empty 'Årsag til eksklusion'
# kommuner_without_arsag = set(all_kommuner) - set(kommuner_with_arsag)

# # Convert to a list or display it
# kommuner_without_arsag = list(kommuner_without_arsag)

# print(f"Kommune(s) with no rows with a value in 'Årsag til eksklusion': {kommuner_without_arsag}")
