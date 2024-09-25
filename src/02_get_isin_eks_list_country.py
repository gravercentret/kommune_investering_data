# %%
import pandas as pd
import re

# Example Danish-English country mapping (you can expand this with more country names)
country_mapping = {
    "Afghanistan": "Afghanistan",
    "Algeriet": "Algeria",
    "Amerikansk Samoa": "American Samoa",
    "Angola": "Angola",
    "Anguilla": "Anguilla",
    "Antigua og Barbuda": "Antigua and Barbuda",
    "Azerbaijan": "Azerbaijan",
    "Bahrain": "Bahrain",
    "Belarus": "Belarus",
    "Benin": "Benin",
    "Bosnien-Hercegovina": "Bosnia and Herzegovina",
    "Burkina Faso": "Burkina Faso",
    "Burundi": "Burundi",
    "Cameroun": "Cameroon",
    "Central Afrikanske Republik": "Central African Republic",
    "Chad": "Chad",
    "Comoros": "Comoros",
    "Congo": "Congo",
    "Congo, Dem. Rep.": "Congo",
    "Congo, Rep.": "Congo",
    "Cuba": "Cuba",
    "De Amerikanske Jomfruøer": "United States Virgin Islands",
    "Democratic People's Republic of Korea": "North Korea",
    "Democratic Republic of the Congo": "Congo",
    "Den Centralafrikanske Republik": "Central African Republic",
    "Den Demokratiske Republik Congo": "Congo",
    "Den Demokratiske Republik Congo (DR Congo)": "Congo",
    "Egypten": "Egypt",
    "Eritrea": "Eritrea",
    "Etiopien": "Ethiopia",
    "Fiji": "Fiji",
    "Forenede Arabiske Emirater (UAE)": "United Arab Emirates",
    "Gabon": "Gabon",
    "Guam": "Guam",
    "Guinea": "Guinea",
    "Guinea-Bissau": "Guinea-Bissau",
    "Haiti": "Haiti",
    "Hviderusland": "Belarus",
    "Irak": "Iraq",
    "Iran": "Iran",
    "Iran (Islamic Republic of)": "Iran",
    "Israel": "Israel",
    "Jordan": "Jordan",
    "Kazakhstan": "Kazakhstan",
    "Kina": "China",
    "Kirgisistan": "Kyrgyzstan",
    "Korea, Dem. Rep.": "North Korea",
    "Laos": "Laos",
    "Lebanon": "Lebanon",
    "Libanon": "Lebanon",
    "Liberia": "Liberia",
    "Libyen": "Libya",
    "Mali": "Mali",
    "Moldova": "Moldova",
    "Mozambique": "Mozambique",
    "Myanmar": "Myanmar",
    "Nicaragua": "Nicaragua",
    "Niger": "Niger",
    "Nigeria": "Nigeria",
    "Nordkorea": "North Korea",
    "Oman": "Oman",
    "Pakistan": "Pakistan",
    "Palau": "Palau",
    "Palæstina": "Palestine",
    "Panama": "Panama",
    "Qatar": "Qatar",
    "Republikken Congo": "Congo",
    "Rusland": "Russia",
    "Russian Federation": "Russia",
    "Rwanda": "Rwanda",
    "Samoa": "Samoa",
    "Saudi Arabien": "Saudi Arabia",
    "Somalia": "Somalia",
    "Sudan": "Sudan",
    "Sydsudan": "South Sudan",
    "Syrian Arab Republic": "Syria",
    "Syrien": "Syria",
    "Tadsjikistan": "Tajikistan",
    "Tajikistan": "Tajikistan",
    "Tchad": "Chad",
    "Togo": "Togo",
    "Trinidad og Tobago": "Trinidad and Tobago",
    "Tunesien": "Tunisia",
    "Turkmenistan": "Turkmenistan",
    "Tyrkiet": "Turkey",
    "Uzbekistan": "Uzbekistan",
    "Vanuatu": "Vanuatu",
    "Venezuela": "Venezuela",
    "Venezuela, RB": "Venezuela",
    "Vestbredden og Gazastriben": "West Bank and Gaza Strip",
    "Vietnam": "Vietnam",
    "Yemen": "Yemen",
    "Yemen, Rep.": "Yemen",
    "Zambia": "Zambia",
    "Zimbabwe": "Zimbabwe",
    "Ækvatorial Guinea": "Equatorial Guinea",
    "Ækvatorialguinea": "Equatorial Guinea",
}


# Utility function to map country name to its English equivalent (strips spaces and ignores case)
def map_country_to_english(country, country_mapping):
    if isinstance(country, str):  # Only process if the country is a string
        country_cleaned = re.sub(
            r"\W+", "", country.strip().lower()
        )  # Remove non-alphanumeric chars, lowercase, strip spaces
        for danish, english in country_mapping.items():
            danish_cleaned = re.sub(r"\W+", "", danish.strip().lower())
            english_cleaned = re.sub(r"\W+", "", english.strip().lower())
            if country_cleaned == danish_cleaned or country_cleaned == english_cleaned:
                return english
    return None  # If not a string or no match, return None


# Function to normalize the names by converting to lowercase but keeping the first letter intact
def normalize_name(name):
    if pd.isna(name):
        return ""
    # Keep the first letter of each word intact, lowercase the rest, and remove special characters
    return " ".join([word.capitalize() for word in re.sub(r"\W+", " ", name).split()])


# Update the function to match multiple ISINs, papers, and udsteder with normalization
def match_country_isin(df1, df2, country_mapping):
    # Apply the country mapping to create a new column with cleaned English country names
    df2["Land oversat"] = df2["Land"].apply(lambda x: map_country_to_english(x, country_mapping))
    df1 = df1[df1["Type"] == "Obligation"]

    # Apply normalization to relevant columns in df1
    df1["Udsteder_normalized"] = df1["Udsteder"].apply(normalize_name)
    df1["Værdipapirets navn_normalized"] = df1["Værdipapirets navn"].apply(normalize_name)

    # Function to find all matching papers, ISINs, and Udsteder
    def find_matches(country, df1):
        if pd.notna(country):
            # Normalize the country name, preserving capitalization of the first letter
            country_normalized = normalize_name(country)

            # Build the regular expression to match whole words with first-letter capitalization
            country_regex = r"\b" + re.escape(country_normalized) + r"\b"

            # Use str.contains with the regex to ensure proper word-boundary matching
            matches = df1[
                df1["Værdipapirets navn_normalized"].str.contains(
                    country_regex, case=True, regex=True, na=False
                )
                | df1["Udsteder_normalized"].str.contains(
                    country_regex, case=True, regex=True, na=False
                )
            ]
            # If matches found, return the unique values for ISIN, 'Værdipapirets navn', and 'Udsteder' as lists
            if not matches.empty:
                isins = matches["ISIN kode"].unique().tolist()
                matching_papers = matches["Værdipapirets navn"].unique().tolist()
                udsteder = matches["Udsteder"].unique().tolist()
                kommune = matches["Kommune"].unique().tolist()
                return isins, matching_papers, udsteder, kommune
        # Return empty lists if country is None or no matches are found
        return [], [], [], []

    # Apply the matching function to each row in df2
    df2[["ISIN", "Matched Værdipapirets navn", "Matched Udsteder", "Kommuner"]] = df2[
        "Land oversat"
    ].apply(lambda country: pd.Series(find_matches(country, df1)))
    print("Done")
    # Return the updated df2 with the new columns
    return df2


data_path = "../data/investeringer_datagrundlag.xlsx"
df = pd.read_excel(data_path)
df_kilde = df[df["ISIN kode"].notna()]

# Akademiker Pension
akademikerpension_path = "../data/Eksklusion_lande/Akademiker Pension_eksklusionsliste_lande.xlsx"
df_akademikerpension = pd.read_excel(akademikerpension_path)

df_akademikerpension_isin = match_country_isin(df_kilde, df_akademikerpension, country_mapping)
file_save = "../data/Eksklusion_lande/Akademiker Pension_eksklusionsliste_lande_isin.xlsx"
df_akademikerpension_isin.to_excel(file_save, index=False)

# AP Pension
APpension_path = "../data/Eksklusion_lande/AP Pension_eksklusionsliste_lande.xlsx"
df_APpension = pd.read_excel(APpension_path)

df_APpension_isin = match_country_isin(df_kilde, df_APpension, country_mapping)
file_save = "../data/Eksklusion_lande/AP Pension_eksklusionsliste_lande_isin.xlsx"
df_APpension_isin.to_excel(file_save, index=False)

# Danske Bank
DanskeBank_path = "../data/Eksklusion_lande/Danske Bank_eksklusionsliste_lande.xlsx"
df_DanskeBank = pd.read_excel(DanskeBank_path)

df_DanskeBank_isin = match_country_isin(df_kilde, df_DanskeBank, country_mapping)
file_save = "../data/Eksklusion_lande/Danske Bank_eksklusionsliste_lande_isin.xlsx"
df_DanskeBank_isin.to_excel(file_save, index=False)

# Industriens Pension
Industrienspension_path = "../data/Eksklusion_lande/Industriens Pension_eksklusionsliste_lande.xlsx"
df_Industrienspension = pd.read_excel(Industrienspension_path)

df_Industrienspension_isin = match_country_isin(df_kilde, df_Industrienspension, country_mapping)
file_save = "../data/Eksklusion_lande/Industriens Pension_eksklusionsliste_lande_isin.xlsx"
df_Industrienspension_isin.to_excel(file_save, index=False)

# Jyske Bank
Jyske_Bank_path = "../data/Eksklusion_lande/Jyske Bank_eksklusionsliste_lande.xlsx"
df_Jyske_Bank = pd.read_excel(Jyske_Bank_path)

df_Jyske_Bank_isin = match_country_isin(df_kilde, df_Jyske_Bank, country_mapping)
file_save = "../data/Eksklusion_lande/Jyske Bank_eksklusionsliste_lande_isin.xlsx"
df_Jyske_Bank_isin.to_excel(file_save, index=False)

# Lægernes Pension
Lægernespension_path = "../data/Eksklusion_lande/Lægernes Pension_eksklusionsliste_lande.xlsx"
df_Lægernespension = pd.read_excel(Lægernespension_path)

df_Lægernespension_isin = match_country_isin(df_kilde, df_Lægernespension, country_mapping)
file_save = "../data/Eksklusion_lande/Lægernes Pension_eksklusionsliste_lande_isin.xlsx"
df_Lægernespension_isin.to_excel(file_save, index=False)

# Lærernes Pension
Lærernespension_path = "../data/Eksklusion_lande/Lærernes Pension_eksklusionsliste_lande.xlsx"
df_Lærernespension = pd.read_excel(Lærernespension_path)

df_Lærernespension_isin = match_country_isin(df_kilde, df_Lærernespension, country_mapping)
file_save = "../data/Eksklusion_lande/Lærernes Pension_eksklusionsliste_lande_isin.xlsx"
df_Lærernespension_isin.to_excel(file_save, index=False)

# PenSam
PenSam_path = "../data/Eksklusion_lande/PenSam_eksklusionsliste_lande.xlsx"
df_PenSam = pd.read_excel(PenSam_path)

df_PenSam_isin = match_country_isin(df_kilde, df_PenSam, country_mapping)
file_save = "../data/Eksklusion_lande/PenSam_eksklusionsliste_lande_isin.xlsx"
df_PenSam_isin.to_excel(file_save, index=False)

# PFA
PFA_path = "../data/Eksklusion_lande/PFA_eksklusionsliste_lande.xlsx"
df_PFA = pd.read_excel(PFA_path)

df_PFA_isin = match_country_isin(df_kilde, df_PFA, country_mapping)
file_save = "../data/Eksklusion_lande/PFA_eksklusionsliste_lande_isin.xlsx"
df_PFA_isin.to_excel(file_save, index=False)

# Sampension
Sampension_path = "../data/Eksklusion_lande/Sampension_eksklusionsliste_lande.xlsx"
df_Sampension = pd.read_excel(Sampension_path)

df_Sampension_isin = match_country_isin(df_kilde, df_Sampension, country_mapping)
file_save = "../data/Eksklusion_lande/Sampension_eksklusionsliste_lande_isin.xlsx"
df_Sampension_isin.to_excel(file_save, index=False)

# Sydinvest
Sydinvest_path = "../data/Eksklusion_lande/Sydinvest_eksklusionsliste_lande.xlsx"
df_Sydinvest = pd.read_excel(Sydinvest_path)

df_Sydinvest_isin = match_country_isin(df_kilde, df_Sydinvest, country_mapping)
file_save = "../data/Eksklusion_lande/Sydinvest_eksklusionsliste_lande_isin.xlsx"
df_Sydinvest_isin.to_excel(file_save, index=False)

# Velliv
Velliv_path = "../data/Eksklusion_lande/Velliv_eksklusionsliste_lande.xlsx"
df_Velliv = pd.read_excel(Velliv_path)

df_Velliv_isin = match_country_isin(df_kilde, df_Velliv, country_mapping)
file_save = "../data/Eksklusion_lande/Velliv_eksklusionsliste_lande_isin.xlsx"
df_Velliv_isin.to_excel(file_save, index=False)


# %%
# import pandas as pd
# import os
# import glob

# # Define the function
# def find_missing_countries(folder_path, country_mapping):
#     # List to hold missing countries from all files
#     missing_countries = []

#     # Function to check if a country is in the mapping
#     def check_country_in_mapping(country, country_mapping):
#         # Strip spaces and convert to uppercase for comparison
#         stripped_country = country.strip().upper()
#         # Also check the stripped and uppercased Danish and English mappings
#         if stripped_country in {k.strip().upper() for k in country_mapping.keys()} or \
#            stripped_country in {v.strip().upper() for v in country_mapping.values()}:
#             return True
#         return False

#     # Get all Excel files ending with '_lande.xlsx' in the folder
#     file_paths = glob.glob(os.path.join(folder_path, '*_lande.xlsx'))

#     # Loop through each file
#     for file_path in file_paths:
#         try:
#             # Load the XLSX file
#             df = pd.read_excel(file_path)

#             # Check if 'Lande' or 'Land' exists in the dataframe
#             if 'Lande' in df.columns:
#                 country_column = 'Lande'
#             elif 'Land' in df.columns:
#                 country_column = 'Land'
#             else:
#                 print(f"Neither 'Lande' nor 'Land' column found in {file_path}")
#                 continue

#             # Iterate over the unique countries in the found column
#             for country in df[country_column].unique():
#                 if not check_country_in_mapping(country, country_mapping):
#                     missing_countries.append(country.strip())
#         except Exception as e:
#             print(f"Error reading {file_path}: {e}")

#     # Get unique missing countries after stripping spaces
#     missing_countries = list(set(missing_countries))

#     # Display the missing countries
#     if missing_countries:
#         print("Missing countries:", missing_countries)
#     else:
#         print("All countries are mapped.")

#     # Optionally, save the missing countries to a file
#     if missing_countries:
#         missing_df = pd.DataFrame(missing_countries, columns=['Missing Countries'])
#         # missing_df.to_csv("missing_countries.csv", index=False)
#         print("Missing countries saved to 'missing_countries.csv'.")
#         return missing_df

# country_mapping = {
#     'Afghanistan': 'AFGHANISTAN',
#     'Azerbaijan': 'AZERBAIJAN',
#     'Algeriet': 'ALGERIA',
#     'Belarus': 'BELARUS',
#     'Benin': 'BENIN',
#     'Burkina Faso': 'BURKINA FASO',
#     'Cameroun': 'CAMEROON',
#     'Chad': 'CHAD',
#     'Cuba': 'CUBA',
#     'Den Centralafrikanske Republik': 'CENTRAL AFRICAN REPUBLIC',
#     'Den Demokratiske Republik Congo': 'DEMOCRATIC REPUBLIC OF CONGO',
#     'Eritrea': 'ERITREA',
#     'Etiopien': 'ETHIOPIA',
#     'Guinea': 'GUINEA',
#     'Irak': 'IRAQ',
#     'Iran': 'IRAN',
#     'Kina': 'CHINA',
#     'Kirgisistan': 'KYRGYZSTAN',
#     'Laos': 'LAOS',
#     'Liberia': 'LIBERIA',
#     'Libyen': 'LIBYA',
#     'Mali': 'MALI',
#     'Myanmar': 'MYANMAR',
#     'Nordkorea': 'NORTH KOREA',
#     'Niger': 'NIGER',
#     'Rusland': 'RUSSIA',
#     'Rwanda': 'RWANDA',
#     'Saudi Arabien': 'SAUDI ARABIA',
#     'Somalia': 'SOMALIA',
#     'Sudan': 'SUDAN',
#     'Sydsudan': 'SOUTH SUDAN',
#     'Syrien': 'SYRIA',
#     'Tajikistan': 'TAJIKISTAN',
#     'Togo': 'TOGO',
#     'Turkmenistan': 'TURKMENISTAN',
#     'Venezuela': 'VENEZUELA',
#     'Yemen': 'YEMEN',
#     'Ækvatorialguinea': 'EQUATORIAL GUINEA'
# }

# # Call the function with the folder path
# folder_path = "../data/Eksklusion_lande"
# missing_df = find_missing_countries(folder_path, country_mapping)


# %%
