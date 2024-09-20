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
            kommune = matches["Kommune"].unique().tolist()
            return isins, udsteder, værdipapirets_navn, kommune
        else:
            return [], [], [], []

    # Apply the function to each row in df2 and create new columns for ISIN, Udsteder, and Værdipapirets navn
    df2[["ISIN", "Matched Udsteder", "Matched Værdipapirets navn", "Kommuner"]] = df2[
        "Selskab_normalized"
    ].apply(lambda x: pd.Series(find_isin_and_names(x, df1)))

    return df2


data_path = "../data/investeringer_datagrundlag.xlsx"
df = pd.read_excel(data_path)
df_kilde = df[df["ISIN kode"].notna()]

# # PFA
# pfa_path = "../data/Eksklusionslister/PFA_eksklusionsliste.xlsx"
# df_pfa = pd.read_excel(pfa_path)

# df_pfa_isin = add_isin_eksklusionsliste(df_kilde, df_pfa)
# file_save = "../data/Eksklusionslister/PFA_eksklusionsliste_isin.xlsx"
# df_pfa_isin.to_excel(file_save, index=False)

# # Akademiker Pension
# akademikerpension_path = "../data/Eksklusionslister/Akademiker Pension_eksklusionsliste.xlsx"
# df_akademikerpension = pd.read_excel(akademikerpension_path)

# df_akademikerpension_isin = add_isin_eksklusionsliste(df_kilde, df_akademikerpension)
# file_save = "../data/Eksklusionslister/Akademiker Pension_eksklusionsliste_isin.xlsx"
# df_akademikerpension_isin.to_excel(file_save, index=False)

# # AP Pension
# appension_path = "../data/Eksklusionslister/AP Pension_eksklusionsliste.xlsx"
# df_appension = pd.read_excel(appension_path)

# df_appension_isin = add_isin_eksklusionsliste(df_kilde, df_appension)
# file_save = "../data/Eksklusionslister/AP Pension_eksklusionsliste_isin.xlsx"
# df_appension_isin.to_excel(file_save, index=False)

# # ATP
# atp_path = "../data/Eksklusionslister/ATP_eksklusionsliste.xlsx"
# df_atp = pd.read_excel(atp_path)

# df_atp_isin = add_isin_eksklusionsliste(df_kilde, df_atp)
# file_save = "../data/Eksklusionslister/ATP_eksklusionsliste_isin.xlsx"
# df_atp_isin.to_excel(file_save, index=False)

# # Lærernes Pension
# lp_path = "../data/Eksklusionslister/Lærernes Pension_eksklusionsliste.xlsx"
# df_lp = pd.read_excel(lp_path)

# df_lp_isin = add_isin_eksklusionsliste(df_kilde, df_lp)
# file_save = "../data/Eksklusionslister/Lærernes Pension_eksklusionsliste_isin.xlsx"
# df_lp_isin.to_excel(file_save, index=False)

# # Nordea
# nordea_path = "../data/Eksklusionslister/Nordea_eksklusionsliste.xlsx"
# df_nordea = pd.read_excel(nordea_path)

# df_nordea_isin = add_isin_eksklusionsliste(df_kilde, df_nordea)
# file_save = "../data/Eksklusionslister/Nordea_eksklusionsliste_isin.xlsx"
# df_nordea_isin.to_excel(file_save, index=False)

# # PensionDanmark
# PensionDanmark_path = "../data/Eksklusionslister/PensionDanmark_eksklusionsliste.xlsx"
# df_PensionDanmark = pd.read_excel(PensionDanmark_path)

# df_PensionDanmark_isin = add_isin_eksklusionsliste(df_kilde, df_PensionDanmark)
# file_save = "../data/Eksklusionslister/PensionDanmark_eksklusionsliste_isin.xlsx"
# df_PensionDanmark_isin.to_excel(file_save, index=False)

# # Sydinvest
# Sydinvest_path = "../data/Eksklusionslister/Sydinvest_eksklusionsliste.xlsx"
# df_Sydinvest = pd.read_excel(Sydinvest_path)

# df_Sydinvest_isin = add_isin_eksklusionsliste(df_kilde, df_Sydinvest)
# file_save = "../data/Eksklusionslister/Sydinvest_eksklusionsliste_isin.xlsx"
# df_Sydinvest_isin.to_excel(file_save, index=False)

# # Velliv
# Velliv_path = "../data/Eksklusionslister/Velliv_eksklusionsliste.xlsx"
# df_Velliv = pd.read_excel(Velliv_path)

# df_Velliv_isin = add_isin_eksklusionsliste(df_kilde, df_Velliv)
# file_save = "../data/Eksklusionslister/Velliv_eksklusionsliste_isin.xlsx"
# df_Velliv_isin.to_excel(file_save, index=False)

# # FN
# FN_path = "../data/Eksklusionslister/FN_eksklusionsliste.xlsx"
# df_FN = pd.read_excel(FN_path)

# df_FN_isin = add_isin_eksklusionsliste(df_kilde, df_FN)
# file_save = "../data/Eksklusionslister/FN_eksklusionsliste_isin.xlsx"
# df_FN_isin.to_excel(file_save, index=False)

# # Jyske Bank
# Jyske_Bank_path = "../data/Eksklusionslister/Jyske Bank_eksklusionsliste.xlsx"
# df_Jyske_Bank = pd.read_excel(Jyske_Bank_path)

# df_Jyske_Bank_isin = add_isin_eksklusionsliste(df_kilde, df_Jyske_Bank)
# file_save = "../data/Eksklusionslister/Jyske Bank_eksklusionsliste_isin.xlsx"
# df_Jyske_Bank_isin.to_excel(file_save, index=False)

# # LD_Fonde
# LD_Fonde_path = "../data/Eksklusionslister/LD Fonde_eksklusionsliste.xlsx"
# df_LD_Fonde = pd.read_excel(LD_Fonde_path)

# df_LD_Fonde_isin = add_isin_eksklusionsliste(df_kilde, df_LD_Fonde)
# file_save = "../data/Eksklusionslister/LD Fonde_eksklusionsliste_isin.xlsx"
# df_LD_Fonde_isin.to_excel(file_save, index=False)

# # Nykredit
# Nykredit_path = "../data/Eksklusionslister/Nykredit_eksklusionsliste.xlsx"
# df_Nykredit = pd.read_excel(Nykredit_path)

# df_Nykredit_isin = add_isin_eksklusionsliste(df_kilde, df_Nykredit)
# file_save = "../data/Eksklusionslister/Nykredit_eksklusionsliste_isin.xlsx"
# df_Nykredit_isin.to_excel(file_save, index=False)

# # PenSam
# PenSam_path = "../data/Eksklusionslister/PenSam_eksklusionsliste.xlsx"
# df_PenSam = pd.read_excel(PenSam_path)

# df_PenSam_isin = add_isin_eksklusionsliste(df_kilde, df_PenSam)
# file_save = "../data/Eksklusionslister/PenSam_eksklusionsliste_isin.xlsx"
# df_PenSam_isin.to_excel(file_save, index=False)

# # Sampension
# Sampension_path = "../data/Eksklusionslister/Sampension_eksklusionsliste.xlsx"
# df_Sampension = pd.read_excel(Sampension_path)

# df_Sampension_isin = add_isin_eksklusionsliste(df_kilde, df_Sampension)
# file_save = "../data/Eksklusionslister/Sampension_eksklusionsliste_isin.xlsx"
# df_Sampension_isin.to_excel(file_save, index=False)

# Lægernes
# Lægernes_path = "../data/Eksklusionslister/Lægernes_eksklusionsliste.xlsx"
# df_Lægernes = pd.read_excel(Lægernes_path)

# df_Lægernes_isin = add_isin_eksklusionsliste(df_kilde, df_Lægernes)
# file_save = "../data/Eksklusionslister/Lægernes_eksklusionsliste_isin.xlsx"
# df_Lægernes_isin.to_excel(file_save, index=False)

# Pædagogernes
# Pædagogernes_path = "../data/Eksklusionslister/Pædagogernes_eksklusionsliste.xlsx"
# df_Pædagogernes = pd.read_excel(Pædagogernes_path)

# df_Pædagogernes_isin = add_isin_eksklusionsliste(df_kilde, df_Pædagogernes)
# df_Pædagogernes_isin['ISIN org'] = df_Pædagogernes['ISIN kode']
# file_save = "../data/Eksklusionslister/Pædagogernes_eksklusionsliste_isin.xlsx"
# df_Pædagogernes_isin.to_excel(file_save, index=False)

# # Spar_Nord
# Spar_Nord_path = "../data/Eksklusionslister/Spar Nord_eksklusionsliste.xlsx"
# df_Spar_Nord = pd.read_excel(Spar_Nord_path)

# df_Spar_Nord_isin = add_isin_eksklusionsliste(df_kilde, df_Spar_Nord)
# file_save = "../data/Eksklusionslister/Spar Nord_eksklusionsliste_isin.xlsx"
# df_Spar_Nord_isin.to_excel(file_save, index=False)

# Industriens
Industriens_path = "../data/Eksklusionslister/Industriens_eksklusionsliste.xlsx"
df_Industriens = pd.read_excel(Industriens_path)

df_Industriens_isin = add_isin_eksklusionsliste(df_kilde, df_Industriens)
file_save = "../data/Eksklusionslister/Industriens_eksklusionsliste_isin.xlsx"
df_Industriens_isin.to_excel(file_save, index=False)