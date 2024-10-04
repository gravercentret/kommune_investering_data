import pandas as pd
from sqlalchemy import create_engine
import numpy as np
from sqlalchemy import create_engine
import polars as pl
import streamlit as st
import pandas as pd
from openai import OpenAI


# # Function to convert dataframe to text
# def dataframe_to_text(df):
#     """
#     This function converts a dataframe into a text format.
#     You can modify it based on how you want to present the data.
#     """
#     text = df.to_json(index=False)  # Convert DataFrame to string (or JSON if needed)
#     return text

# def create_unique_reasons_list(df):
#     årsager = set(df['Eksklusionsårsager'].tolist())

#     # Step 1: Flatten the list by splitting each string on the semicolon
#     flattened_topics = [topic.strip() for item in årsager for topic in item.split(';')]

#     # Step 2: Create a set to store unique topics
#     unique_topics = set(flattened_topics)

#     # Step 3: If necessary, you can sort or further process the unique topics
#     # Sort for presentation purposes
#     unique_topics = sorted(unique_topics)

#     return unique_topics

# # Function to generate text using OpenAI API
# def generate_text_from_dataframe(
#     api_key,
#     prompt_template="",
#     system_prompt="",
# ):
#     """
#     Takes a dataframe and sends it to the OpenAI API to generate text.
#     """

#     # Convert dataframe to a string format (you can customize this part)
#     # df_text = dataframe_to_text(df)

#     # Create a prompt by combining the template and the dataframe text
#     prompt = f'{prompt_template}'

#     client = OpenAI(api_key=api_key)

#     completion = client.chat.completions.create(
#         model="gpt-4o-mini",
#         messages=[
#             {"role": "system", "content": system_prompt},
#             {"role": "user", "content": prompt},
#         ],
#     )

#     return completion.choices[0].message

# def create_area_text(df, api_key):

#     area_summaries = []

#     system_prompt = """Du er en assistent, der skal hjælpe en journalist.
#     Du får en liste med forskellige eksklusionsårsager.
#     Skab et overblik selv, og præsentér opsummeringen i punktform.
#     Besvar udelukkende med punkterne, ikke med en overskrift eller afsluttende bemærkning.
#     """

#     unique_areas = set(df['Kommune'].tolist())
#     for area in unique_areas:

#         df_filtered = df[df["Kommune"] == area]
#         df_filtered = df_filtered[df_filtered["Problematisk ifølge:"].notna()]

#         årsager = create_unique_reasons_list(df_filtered)

#         prompt_template = f"""Lav en opsummering af eksklusionsårsagerne, og de overordnede årsager.
#         Det skal være i punktform. Det handler om investeringer foretaget af {area}.
#         Det hele skal stå på dansk. Undgå gentagelser.
#         Her er årsagerne:
#         {årsager}
#         Hvis der ikke er nogen årsag, så skriv, at der ikke er noget relevant data.
#         """
#         print(area)
#         result = generate_text_from_dataframe(api_key, prompt_template, system_prompt)

#         area_summaries.append({"Kommune": area, "Resumé": result.content})
#     df_summaries = pd.DataFrame(area_summaries)
#     return df_summaries

# # Your OpenAI API key (replace with your actual key)
# with open("../dev/api_key.txt") as f:
#     api_key = f.read()


# data_path = "../data/full_data.xlsx"
# df = pd.read_excel(data_path)
# # df_only_prop = df[df["Problematisk ifølge:"].notna()]
# df_sort = df.sort_values('Kommune')
# # df_sort = df_sort.head(10000)
# df_summaries = create_area_text(df_sort, api_key)

# df_summaries.to_csv("første_udkast_ai_tekster.csv")


# # Create an SQLite engine
engine = create_engine("sqlite:///investerings_database_encrypted_new.db")

# # Save the DataFrame 'df' to the SQLite database
# # 'data_table' is the name of the table that will be created in the database
df_summaries.to_sql("kommunale_regioner_ai_tekster", engine, if_exists="replace", index=False)

# print("DataFrame has been saved to SQLite database as 'data_table'.")

# Example of a query to retrieve data from the local SQLite database
# Connect to the SQLite database
with engine.connect() as conn:
    # Sample query to select all rows
    query = "SELECT * FROM kommunale_regioner_ai_tekster;"  # Example query

    df_resumé = pd.read_sql(query, conn)

print(df_resumé)

data_path = "Kontrolforsøg_ai_text_samlet.xlsx"
df_errors = pd.read_excel(data_path)
df_errors = df_errors[df_errors["Kommune"].notna()]
df_errors["Kommune"] = df_errors["Kommune"].str.strip()
df_errors["Fjern"] = df_errors["Fjern"].str.strip()
df_errors["Ændring"] = df_errors["Ændring"].str.strip()


# Function to clean up the resumé
def clean_resumé(kommune, resumé, df_errors):
    # Get the row in df_errors that matches the kommune
    
    error_rows = df_errors[df_errors["Kommune"] == kommune]
    if not error_rows.empty:
        # Loop through each error row
        for _, error_row in error_rows.iterrows():
            text_to_remove = error_row["Fjern"]
            replacement = error_row["Ændring"]

            # Only proceed if text_to_remove is a string and exists in the resumé
            if isinstance(text_to_remove, str) and text_to_remove in resumé:
                # If there is a replacement and it's valid, replace the text
                if isinstance(replacement, str) and replacement.strip():
                    resumé = resumé.replace(text_to_remove, replacement)
                else:
                    # Handle newline and space cleanup
                    resumé = resumé.replace(f"\n  - {text_to_remove}", "") \
                                .replace(f"- {text_to_remove}", "") \
                                .replace(f"- {text_to_remove}\n", "")

        # After all removals, clean up consecutive newlines
        resumé = '\n'.join([line for line in resumé.split('\n') if line.strip()])

    
    resumé = resumé.replace("- Overordnede årsager: \n", "")
    resumé = resumé.replace("- Eksklusionsårsager: \n", "")
    resumé = resumé.replace("\n\nOverordnede årsager:", "")
    resumé = resumé.replace("\n\n- Eksklusionsårsager:", "")
    return resumé
# Apply the function to clean up the resumé for each row in df_resumé
df_resumé["Resumé_renset"] = df_resumé.apply(
    lambda row: clean_resumé(row["Kommune"], row["Resumé"], df_errors), axis=1
)
df_resumé.loc[df_resumé['Kommune'] == 'Greve', 'Resumé_renset'] = df_resumé.loc[df_resumé['Kommune'] == 'Greve', 'Resumé_renset'].iloc[0] + "\n- Naturressourcer"
df_resumé.loc[df_resumé['Kommune'] == 'Svendborg', 'Resumé_renset'] = df_resumé.loc[df_resumé['Kommune'] == 'Svendborg', 'Resumé_renset'].iloc[0] + "\n- Støtte til tjenester og forsyninger i besættelsesområder\n- Våben"


####

df_resumé['Resumé'] = df_resumé['Resumé_renset']
df_resumé.drop('Resumé_renset', axis=1, inplace=True)

engine = create_engine("sqlite:///investerings_database_encrypted_new.db")

# # Save the DataFrame 'df' to the SQLite database
# # 'data_table' is the name of the table that will be created in the database
df_resumé.to_sql("kommunale_regioner_ai_tekster", engine, if_exists="replace", index=False)


# Print the updated dataframe
# print(df_resumé)

# import re 

# def clean_resumé_alle_kommuner_with_replacement(resumé, df_errors):
#     # Get rows that apply to all kommuner and have a valid replacement
#     error_rows_all = df_errors[(df_errors['Kommune'] == 'Alle kommuner') & 
#                                (df_errors['Ændring'].notna())]
    
#     if not error_rows_all.empty:
#         # Loop through each error row in 'Alle kommuner' with a replacement
#         for _, error_row in error_rows_all.iterrows():
#             text_to_remove = error_row['Fjern']
#             replacement = error_row['Ændring']
            
#             # Only proceed if text_to_remove and replacement are valid strings
#             if isinstance(text_to_remove, str) and isinstance(replacement, str) and replacement.strip():
#                 # Create regex to match the entire line that contains "- {text_to_remove}\n" or "- {text_to_remove} \n"
#                 pattern = rf"(?m)^\s*- {re.escape(text_to_remove)} ?\n"
                
#                 # Replace the found text with the replacement, ensuring the entire line is replaced
#                 resumé = re.sub(pattern, f"- {replacement}\n", resumé)
        
#         # Clean up consecutive newlines
#         resumé = '\n'.join([line for line in resumé.split('\n') if line.strip()])
    
#     # Return the updated resumé (or original if no match was found)
#     return resumé

# # Example usage of the new function:
# # Apply the function to clean up 'Alle kommuner' entries with replacements for each row in df_resumé
# df_resumé['Resumé_renset'] = df_resumé['Resumé_renset'].apply(lambda res: clean_resumé_alle_kommuner_with_replacement(res, df_errors))

df_resumé.to_excel("ai_text_corrected.xlsx")

###
# Create an SQLite engine
engine = create_engine("sqlite:///investerings_database_ai_tekster.db")

# Save the DataFrame 'df' to the SQLite database
# 'data_table' is the name of the table that will be created in the database
df_resumé.to_sql("kommunale_regioner_ai_tekster", engine, if_exists="replace", index=False)

print("DataFrame has been saved to SQLite database as 'data_table'.")

engine = create_engine("sqlite:///investerings_database.db")

# Save the DataFrame 'df' to the SQLite database
# 'data_table' is the name of the table that will be created in the database
df_resumé.to_sql("kommunale_regioner_ai_tekster", engine, if_exists="replace", index=False)

print("DataFrame has been saved to SQLite database as 'data_table'.")