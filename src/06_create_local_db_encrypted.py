import pandas as pd
from sqlalchemy import create_engine
from cryptography.fernet import Fernet
import os
from dotenv import load_dotenv  # Required if using .env file

# Optional: load environment variables from a .env file
load_dotenv()

# Fetch the key from environment variables
encryption_key = os.getenv("ENCRYPTION_KEY")

cipher_suite = Fernet(encryption_key)


def encrypt_dataframe(df, cipher_suite, col_list):
    df_encrypted = df.copy()  # Create a copy of the DataFrame

    for col in col_list:
        if pd.api.types.is_numeric_dtype(df_encrypted[col]):
            # Encrypt numeric columns (convert to string first)
            df_encrypted[col] = df_encrypted[col].apply(
                lambda x: cipher_suite.encrypt(str(x).encode()).decode()
            )
        elif pd.api.types.is_string_dtype(df_encrypted[col]):
            # Encrypt string columns
            df_encrypted[col] = df_encrypted[col].apply(
                lambda x: cipher_suite.encrypt(x.encode()).decode()
            )
        else:
            # Convert non-numeric, non-string columns to string and then encrypt
            df_encrypted[col] = df_encrypted[col].apply(
                lambda x: cipher_suite.encrypt(str(x).encode()).decode()
            )

    return df_encrypted


data_path = "../data/full_data.xlsx"
df = pd.read_excel(data_path)

# Choose which columns to send to database
df_to_db = df[
    [
        "Kommune",
        "ISIN kode",
        "Værdipapirets navn",
        "Udsteder",
        "Markedsværdi (DKK)",
        "Type",
        "Årsag til eksklusion",
        "OBS_Type",
        "Priority",
        "Problematisk ifølge:",
    ]
]

# Only encrypt the nessecary columns
col_list = ["Kommune", "ISIN kode", "Værdipapirets navn"]

# Encrypt the dataframe
df_encrypted = encrypt_dataframe(df_to_db, cipher_suite, col_list)

# Create an SQLite engine
engine = create_engine("sqlite:///investerings_database_encrypted.db")

# Save the DataFrame 'df' to the SQLite database
# 'data_table' is the name of the table that will be created in the database
df_encrypted.to_sql("kommunale_regioner_investeringer", engine, if_exists="replace", index=False)

print("DataFrame has been saved to SQLite database as 'data_table'.")


# import gzip
# import shutil

# # Compress the database
# with open("investerings_database_encrypted.db", "rb") as f_in:
#     with gzip.open("investerings_database_encrypted.db.gz", "wb") as f_out:
#         shutil.copyfileobj(f_in, f_out)

# print("Database compressed.")

# # Decompress the database
# with gzip.open("investerings_database_encrypted.db.gz", "rb") as f_in:
#     with open("investerings_database_encrypted_decompressed.db", "wb") as f_out:
#         shutil.copyfileobj(f_in, f_out)

# print("Database decompressed.")
