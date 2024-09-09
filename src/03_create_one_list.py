import os
import pandas as pd
import ast

# Define the folder where your files are located
folder_path = '../data/Eksklusionslister/'

# Step 1: Identify files ending with _isin.xlsx
isin_files = [file for file in os.listdir(folder_path) if file.endswith('_isin.xlsx')]

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
    file_prefix = file.split('_')[0]
    
    df = pd.read_excel(file_path)
    
    # Select only the required columns
    df = df[['Selskab', 'Årsag til eksklusion', 'Selskab_normalized', 'ISIN', 'Matched Udsteder', 'Matched Værdipapirets navn']]
    
    # Step 3: Modify 'Årsag til eksklusion' by adding the file prefix at the beginning
    df['Årsag til eksklusion'] = df['Årsag til eksklusion'].apply(lambda x: f"{file_prefix}: {x}")
    
    # Step 4: Filter rows where ISIN is not empty and safely explode the ISIN list into separate rows
    df['ISIN'] = df['ISIN'].apply(safe_eval_isin)  # Safely convert ISIN string to list
    df = df[df['ISIN'].apply(lambda x: len(x) > 0)]  # Filter rows where ISIN list is not empty
    df = df.explode('ISIN')  # Create a new row for each ISIN
    
    # Ensure ISIN is a string (since it may still be a list element after explode)
    df['ISIN'] = df['ISIN'].astype(str)
    
    # Step 5: Append the cleaned DataFrame to the list
    dataframes.append(df)

# Step 6: Concatenate all dataframes
final_df = pd.concat(dataframes, ignore_index=True)

# Save the final dataframe to a new Excel file if needed
final_df.to_excel('filtered_isin_data_with_prefix.xlsx', index=False)

# Print the resulting DataFrame
print(final_df)

# Step 7: Collapse rows with the same ISIN
# Function to merge differing values into a semicolon-separated string
def merge_values(series):
    unique_vals = series.dropna().unique()
    if len(unique_vals) == 1:
        return unique_vals[0]  # If only one unique value, return it
    else:
        return "; ".join(unique_vals)  # If multiple values, join them with a semicolon

# Group by ISIN and apply the merging function to each column
collapsed_df = final_df.groupby('ISIN').agg({
    'Selskab': merge_values,
    'Årsag til eksklusion': merge_values,
    'Selskab_normalized': merge_values,
    'Matched Udsteder': merge_values,
    'Matched Værdipapirets navn': merge_values
}).reset_index()

# Save the collapsed dataframe to a new Excel file
collapsed_df.to_excel('collapsed_isin_data.xlsx', index=False)

# Print the resulting DataFrame
print(collapsed_df)
