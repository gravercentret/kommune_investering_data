import pandas as pd

data_path = "../data/data_investeringer.xlsx"
df = pd.read_excel(data_path)
df_kilde = df[df['ISIN kode'].notna()]

isin_path = "all_exclude_lists_isin.xlsx"
df_isin = pd.read_excel(isin_path)

# Perform a left merge on the 'ISIN kode' from df_kilde and 'ISIN' from df_isin
merged_df = pd.merge(df_kilde, df_isin, how='left', left_on='ISIN kode', right_on='ISIN')

# Save the merged DataFrame to a new Excel file if needed
merged_df.to_excel('merged_data.xlsx', index=False)

# Print the resulting DataFrame
print(merged_df)

