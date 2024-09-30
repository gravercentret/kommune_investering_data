# from cryptography.fernet import Fernet

# # Generate a new encryption key
# key = Fernet.generate_key()

# # Save this key somewhere secure; you will need it to decrypt the data
# print(key.decode())  # Outputs the key as a string

import os
from cryptography.fernet import Fernet
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv  # Required if using .env file

# Optional: load environment variables from a .env file
load_dotenv()

# Fetch the key from environment variables
encryption_key = os.getenv("ENCRYPTION_KEY")

# Initialize the Fernet cipher suite with the key
cipher_suite = Fernet(encryption_key)


# Define functions to encrypt and decrypt the columns
def encrypt_column(data, cipher_suite):
    return data.apply(lambda x: cipher_suite.encrypt(x.encode()).decode())


def decrypt_column(data, cipher_suite):
    return data.apply(lambda x: cipher_suite.decrypt(x.encode()).decode())


# Load your Excel data
data_path = "../data/full_data.xlsx"
df = pd.read_excel(data_path)

# Choose columns to encrypt (example: encrypting 'Værdipapirets navn')
df["Værdipapirets navn"] = encrypt_column(df["Værdipapirets navn"], cipher_suite)

# Create an SQLite engine and save the encrypted DataFrame
engine = create_engine("sqlite:///investerings_database_test.db")
df.to_sql("kommunale_regioner_investeringer", engine, if_exists="replace", index=False)

print("Encrypted DataFrame has been saved to SQLite database.")

# Later, when retrieving the data
df_retrieved = pd.read_sql("SELECT * FROM kommunale_regioner_investeringer_test", engine)

# Decrypt the 'Værdipapirets navn' column after loading
df_retrieved["Værdipapirets navn"] = decrypt_column(
    df_retrieved["Værdipapirets navn"], cipher_suite
)

# Show the decrypted data
print(df_retrieved.head())
