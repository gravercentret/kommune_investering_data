# %% Akademiker Pension
import pandas as pd

# Path to the uploaded file
path = "../data/Eksklusion_lande/Akademiker Pension_eksklusionsliste_lande_x.xlsx"

df_with_x = pd.read_excel(path)


# Create a new column 'Årsag til eksklusion'
def create_exclusion_reason(row):
    reasons = []
    if row["Menneskerettigheder"] == "X":
        reasons.append("Menneskerettigheder")
    if row["Klima"] == "X":
        reasons.append("Klima")
    return "; ".join(reasons)


df_with_x["Årsag til eksklusion"] = df_with_x.apply(create_exclusion_reason, axis=1)

df = pd.DataFrame()
df = df_with_x[["Land", "Årsag til eksklusion"]]

# Save the updated DataFrame to a new Excel file
output_file_path = "../data/Eksklusion_lande/Akademiker Pension_eksklusionsliste_lande.xlsx"
df.to_excel(output_file_path, index=False)

# %%
