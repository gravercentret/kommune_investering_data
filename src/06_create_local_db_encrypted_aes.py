import pandas as pd
from sqlalchemy import create_engine
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
import os
from dotenv import load_dotenv  # Required if using .env file
import base64

# Optional: load environment variables from the .env file
load_dotenv()

# Fetch the base64 encoded key from environment variables
encoded_key = os.getenv("ENCRYPTION_KEY")

# Decode the key back to bytes for AES use
encryption_key = base64.b64decode(encoded_key)

# Encrypt data using AES-CBC mode
def aes_encrypt(data, key):
    iv = os.urandom(16)  # Initialization vector for CBC mode
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()

    # Add padding (AES requires block size of 128 bits, or 16 bytes)
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(data.encode()) + padder.finalize()

    encrypted_data = encryptor.update(padded_data) + encryptor.finalize()
    return base64.b64encode(iv + encrypted_data).decode()  # Return Base64 encoded IV + ciphertext

# Decrypt data using AES-CBC mode
def aes_decrypt(encrypted_data, key):
    encrypted_data = base64.b64decode(encrypted_data.encode())  # Decode Base64 to bytes
    iv = encrypted_data[:16]  # Extract the first 16 bytes as the IV
    ciphertext = encrypted_data[16:]
    
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()

    decrypted_padded_data = decryptor.update(ciphertext) + decryptor.finalize()

    # Remove padding
    unpadder = padding.PKCS7(128).unpadder()
    decrypted_data = unpadder.update(decrypted_padded_data) + unpadder.finalize()

    return decrypted_data.decode()

# Function to encrypt specified columns of the DataFrame using AES-CBC
def encrypt_dataframe(df, key, col_list):
    df_encrypted = df.copy()  # Create a copy of the DataFrame

    for col in col_list:
        if pd.api.types.is_numeric_dtype(df_encrypted[col]):
            # Encrypt numeric columns (convert to string first)
            df_encrypted[col] = df_encrypted[col].apply(
                lambda x: print(f"Encrypting: {x}") or aes_encrypt(str(x), key)
            )
        elif pd.api.types.is_string_dtype(df_encrypted[col]):
            # Encrypt string columns
            df_encrypted[col] = df_encrypted[col].apply(
                lambda x: print(f"Encrypting: {x}") or aes_encrypt(x, key)
            )
        else:
            # Convert non-numeric, non-string columns to string and then encrypt
            df_encrypted[col] = df_encrypted[col].apply(
                lambda x: print(f"Encrypting: {x}") or aes_encrypt(str(x), key)
            )

    return df_encrypted

# Function to decrypt specified columns of the DataFrame using AES-CBC
def decrypt_dataframe(df, key, col_list):
    df_decrypted = df.copy()  # Create a copy of the DataFrame

    for col in col_list:
        if pd.api.types.is_string_dtype(df_decrypted[col]):
            # Decrypt string columns
            df_decrypted[col] = df_decrypted[col].apply(
                lambda x: aes_decrypt(x, key)
            )
        else:
            # Convert to the original data type after decryption
            df_decrypted[col] = df_decrypted[col].apply(
                lambda x: aes_decrypt(str(x), key)
            )

    return df_decrypted


# Load data
data_path = "../data/full_data.xlsx"
df = pd.read_excel(data_path)

# Choose which columns to send to the database
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
        "Eksklusionsårsager",
    ]
]

# Only encrypt the necessary columns
col_list = ["Kommune", "ISIN kode", "Værdipapirets navn"]

# Encrypt the dataframe
df_encrypted = encrypt_dataframe(df_to_db, encryption_key, col_list)

# Create an SQLite engine
engine = create_engine("sqlite:///investerings_database_encrypted_new.db")

# Save the encrypted DataFrame to the SQLite database
df_encrypted.to_sql("kommunale_regioner_investeringer", engine, if_exists="replace", index=False)

print("Encrypted DataFrame has been saved to SQLite database as 'kommunale_regioner_investeringer'.")

# --- Optional: Decrypt the DataFrame for verification ---
df_retrieved = pd.read_sql("SELECT * FROM kommunale_regioner_investeringer", engine)
df_decrypted = decrypt_dataframe(df_retrieved, encryption_key, col_list)
print("Decrypted DataFrame:")
print(df_decrypted.head())

