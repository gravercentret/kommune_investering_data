import pandas as pd
import re


def add_isin_eksklusionsliste(df_kilde, df_eksklusionsliste):
    # Sample data
    df1 = df_kilde
    df2 = df_eksklusionsliste

    # Normalize company names by converting to lowercase and removing special characters
    def normalize_name(name):
        if pd.isna(name):
            return ""
        # Lowercase and remove special characters
        return re.sub(r"\W+", "", name.lower())

    # Apply normalization to relevant columns
    df1["Udsteder_normalized"] = df1["Udsteder"].apply(normalize_name)
    df1["Værdipapirets navn_normalized"] = df1["Værdipapirets navn"].apply(normalize_name)
    df2["Selskab_normalized"] = df2["Selskab"].apply(normalize_name)

    # Function to find ISINs, Udsteder, and Værdipapirets navn based on partial match
    def find_isin_and_names(selskab, df1):
        matches = df1[
            (df1["Udsteder_normalized"].str.contains(selskab))
            | (df1["Værdipapirets navn_normalized"].str.contains(selskab))
        ]
        # Return unique ISINs, Udsteder, and Værdipapirets navn if matches are found
        if not matches.empty:
            isins = matches["ISIN kode"].unique().tolist()
            udsteder = matches["Udsteder"].unique().tolist()
            værdipapirets_navn = matches["Værdipapirets navn"].unique().tolist()
            return isins, udsteder, værdipapirets_navn
        else:
            return [], [], []

    # Apply the function to each row in df2 and create new columns for ISIN, Udsteder, and Værdipapirets navn
    df2[["ISIN", "Matched Udsteder", "Matched Værdipapirets navn"]] = df2[
        "Selskab_normalized"
    ].apply(lambda x: pd.Series(find_isin_and_names(x, df1)))

    return df2


data_path = "../data/data_investeringer.xlsx"
df = pd.read_excel(data_path)
df_kilde = df[df["ISIN kode"].notna()]

# PFA
pfa_path = "../data/Eksklusionslister/PFA_eksklusionsliste.xlsx"
df_pfa = pd.read_excel(pfa_path)

df_pfa_isin = add_isin_eksklusionsliste(df_kilde, df_pfa)
file_save = "../data/Eksklusionslister/PFA_eksklusionsliste_isin.xlsx"
df_pfa_isin.to_excel(file_save, index=False)

# Akademiker Pension
akademikerpension_path = "../data/Eksklusionslister/Akademiker Pension_eksklusionsliste.xlsx"
df_akademikerpension = pd.read_excel(akademikerpension_path)

df_akademikerpension_isin = add_isin_eksklusionsliste(df_kilde, df_akademikerpension)
file_save = "../data/Eksklusionslister/Akademiker Pension_eksklusionsliste_isin.xlsx"
df_akademikerpension_isin.to_excel(file_save, index=False)

# AP Pension
appension_path = "../data/Eksklusionslister/AP Pension_eksklusionsliste.xlsx"
df_appension = pd.read_excel(appension_path)

df_appension_isin = add_isin_eksklusionsliste(df_kilde, df_appension)
file_save = "../data/Eksklusionslister/AP Pension_eksklusionsliste_isin.xlsx"
df_appension_isin.to_excel(file_save, index=False)

# ATP
atp_path = "../data/Eksklusionslister/ATP_eksklusionsliste.xlsx"
df_atp = pd.read_excel(atp_path)

df_atp_isin = add_isin_eksklusionsliste(df_kilde, df_atp)
file_save = "../data/Eksklusionslister/ATP_eksklusionsliste_isin.xlsx"
df_atp_isin.to_excel(file_save, index=False)

# Lærernes Pension
lp_path = "../data/Eksklusionslister/Lærernes Pension_eksklusionsliste.xlsx"
df_lp = pd.read_excel(lp_path)

df_lp_isin = add_isin_eksklusionsliste(df_kilde, df_lp)
file_save = "../data/Eksklusionslister/Lærernes Pension_eksklusionsliste_isin.xlsx"
df_lp_isin.to_excel(file_save, index=False)

# Nordea
nordea_path = "../data/Eksklusionslister/Nordea_eksklusionsliste.xlsx"
df_nordea = pd.read_excel(nordea_path)

df_nordea_isin = add_isin_eksklusionsliste(df_kilde, df_nordea)
file_save = "../data/Eksklusionslister/Nordea_eksklusionsliste_isin.xlsx"
df_nordea_isin.to_excel(file_save, index=False)

# PensionDanmark
PensionDanmark_path = "../data/Eksklusionslister/PensionDanmark_eksklusionsliste.xlsx"
df_PensionDanmark = pd.read_excel(PensionDanmark_path)

df_PensionDanmark_isin = add_isin_eksklusionsliste(df_kilde, df_PensionDanmark)
file_save = "../data/Eksklusionslister/PensionDanmark_eksklusionsliste_isin.xlsx"
df_PensionDanmark_isin.to_excel(file_save, index=False)

# Sydinvest
Sydinvest_path = "../data/Eksklusionslister/Sydinvest_eksklusionsliste.xlsx"
df_Sydinvest = pd.read_excel(Sydinvest_path)

df_Sydinvest_isin = add_isin_eksklusionsliste(df_kilde, df_Sydinvest)
file_save = "../data/Eksklusionslister/Sydinvest_eksklusionsliste_isin.xlsx"
df_Sydinvest_isin.to_excel(file_save, index=False)

# Velliv
Velliv_path = "../data/Eksklusionslister/Velliv_eksklusionsliste.xlsx"
df_Velliv = pd.read_excel(Velliv_path)

df_Velliv_isin = add_isin_eksklusionsliste(df_kilde, df_Velliv)
file_save = "../data/Eksklusionslister/Velliv_eksklusionsliste_isin.xlsx"
df_Velliv_isin.to_excel(file_save, index=False)

# FN
FN_path = "../data/Eksklusionslister/FN_eksklusionsliste.xlsx"
df_FN = pd.read_excel(FN_path)

df_FN_isin = add_isin_eksklusionsliste(df_kilde, df_FN)
file_save = "../data/Eksklusionslister/FN_eksklusionsliste_isin.xlsx"
df_FN_isin.to_excel(file_save, index=False)
