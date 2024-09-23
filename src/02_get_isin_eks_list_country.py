#%%
import pandas as pd
import re

# Example Danish-English country mapping (you can expand this with more country names)
country_mapping = {
    'Afghanistan': 'AFGHANISTAN',
    'Azerbaijan': 'AZERBAIJAN',
    'Algeriet': 'ALGERIA',
    'Belarus': 'BELARUS',
    'Benin': 'BENIN',
    'Burkina Faso': 'BURKINA FASO',
    'Cameroun': 'CAMEROON',
    'Chad': 'CHAD',
    'Cuba': 'CUBA',
    'Den Centralafrikanske Republik': 'CENTRAL AFRICAN REPUBLIC',
    'Den Demokratiske Republik Congo': 'DEMOCRATIC REPUBLIC OF CONGO',
    'Eritrea': 'ERITREA',
    'Etiopien': 'ETHIOPIA',
    'Guinea': 'GUINEA',
    'Irak': 'IRAQ',
    'Iran': 'IRAN',
    'Kina': 'CHINA',
    'Kirgisistan': 'KYRGYZSTAN',
    'Laos': 'LAOS',
    'Liberia': 'LIBERIA',
    'Libyen': 'LIBYA',
    'Mali': 'MALI',
    'Myanmar': 'MYANMAR',
    'Nordkorea': 'NORTH KOREA',
    'Niger': 'NIGER',
    'Rusland': 'RUSSIA',
    'Rwanda': 'RWANDA',
    'Saudi Arabien': 'SAUDI ARABIA',
    'Somalia': 'SOMALIA',
    'Sudan': 'SUDAN',
    'Sydsudan': 'SOUTH SUDAN',
    'Syrien': 'SYRIA',
    'Tajikistan': 'TAJIKISTAN',
    'Togo': 'TOGO',
    'Turkmenistan': 'TURKMENISTAN',
    'Venezuela': 'VENEZUELA',
    'Yemen': 'YEMEN',
    'Ækvatorialguinea': 'EQUATORIAL GUINEA'
}

# Create a function to map Danish country to the English equivalent
def map_country_to_english(danish_country, country_mapping):
    return country_mapping.get(danish_country, None)

def match_country_isin(df1, df2, country_mapping):
    df1= df1[df1['Type'] == 'Obligation']

    # Apply the country mapping to create a new column with English country names
    df2['English Land'] = df2['Land'].apply(lambda x: map_country_to_english(x, country_mapping))

    # Merge based on the match of the English country names with 'Værdipapirets navn' in df1
    df2['Matching Paper'] = df2['English Land'].apply(lambda country: df1[df1['Værdipapirets navn'].str.contains(country, case=False)]['Værdipapirets navn'].values[0] if pd.notnull(country) and df1['Værdipapirets navn'].str.contains(country, case=False).any() else None)

    df2['ISIN'] = df2['English Land'].apply(lambda country: df1[df1['Værdipapirets navn'].str.contains(country, case=False)]['ISIN kode'].values[0] if pd.notnull(country) and df1['Værdipapirets navn'].str.contains(country, case=False).any() else None)

    df2['Matching Udsteder'] = df2['English Land'].apply(lambda country: df1[df1['Værdipapirets navn'].str.contains(country, case=False)]['Udsteder'].values[0] if pd.notnull(country) and df1['Værdipapirets navn'].str.contains(country, case=False).any() else None)

    # The resulting dataframe will have the new columns with ISIN and matching Værdipapirets navn
    return df2


data_path = "../data/investeringer_datagrundlag.xlsx"
df = pd.read_excel(data_path)
df_kilde = df[df["ISIN kode"].notna()]

# Akademiker Pension 
# akademikerpension_path = "../data/Eksklusion_lande/Akademiker Pension_eksklusionsliste_lande.xlsx"
# df_akademikerpension = pd.read_excel(akademikerpension_path)

# df_akademikerpension_isin = match_country_isin(df_kilde, df_akademikerpension, country_mapping)
# file_save = "../data/Eksklusion_lande/Akademiker Pension_eksklusionsliste_lande_isin.xlsx"
# df_akademikerpension_isin.to_excel(file_save, index=False)


# %%
