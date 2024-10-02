import numpy as np
from sqlalchemy import create_engine
import polars as pl
import streamlit as st
import pandas as pd
from openai import OpenAI


def get_data():
    engine = create_engine("sqlite:///../src/investerings_database.db")

    query = """
        SELECT [Kommune], [Udsteder], [Værdipapirets navn], [Markedsværdi (DKK)], [Type], 
        [Problematisk ifølge:], 
        [Årsag til eksklusion], [Eksklusionsårsager]
        FROM kommunale_regioner_investeringer;
    """

    # Execute the query and load the result into a Polars DataFrame
    with engine.connect() as conn:
        df_polars = pl.read_database(query, conn)

    return df_polars


# Function to convert dataframe to text
def dataframe_to_text(df):
    """
    This function converts a dataframe into a text format.
    You can modify it based on how you want to present the data.
    """
    text = df.to_json(index=False)  # Convert DataFrame to string (or JSON if needed)
    return text


# Function to generate text using OpenAI API
def generate_text_from_dataframe(
    df,
    api_key,
    prompt_template="",
    system_prompt="Du er en assistent, der skal svare på dansk og hjælpe journalister.",
):
    """
    Takes a dataframe and sends it to the OpenAI API to generate text.
    """

    # Convert dataframe to a string format (you can customize this part)
    df_text = dataframe_to_text(df)

    # Create a prompt by combining the template and the dataframe text
    prompt = f"{prompt_template}\n\n{df_text}"

    client = OpenAI(api_key=api_key)

    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt},
        ],
    )

    # Extract the generated text
    # generated_text = completion.choices[0].text.strip()
    print(completion.choices[0].message)

    return completion.choices[0].message


system_prompt = """Du er en assistent, der skal hjælpe en journalist. 
    Du får en liste med forskellige temaer.
    Lav et resumé af disse i punktform. 
    Besvar udelukkende med punkter, ikke med en overskrift.
    """

# Your OpenAI API key (replace with your actual key)
with open("api_key.txt") as f:
    api_key = f.read()

# Get data
df_pl = get_data()
df_pd = df_pl.to_pandas()
kommune = "Tønder"
df_test = df_pd[df_pd["Kommune"] == kommune]
# antal_inv = len(df_test)
# sum_inv = sum(df_test["Markedsværdi (DKK)"])
# antal_inv_prop = len(df_test[df_test["Problematisk ifølge:"].notna()])
# sum_inv_prop = sum(df_test[df_test["Problematisk ifølge:"].notna()]["Markedsværdi (DKK)"])


def create_unique_reasons_list(df):
    årsager = set(df_prop["Eksklusionsårsager"].tolist())

    # Step 1: Flatten the list by splitting each string on the semicolon
    flattened_topics = [topic.strip() for item in årsager for topic in item.split(";")]

    # Step 2: Create a set to store unique topics
    unique_topics = set(flattened_topics)

    # Step 3: If necessary, you can sort or further process the unique topics
    # Sort for presentation purposes
    unique_topics = sorted(unique_topics)

    return unique_topics


df_prop = df_test[df_test["Problematisk ifølge:"].notna()]

årsager = create_unique_reasons_list(df_prop)

prompt_template = f"""Lav en gengivelse eksklusionsårsagerne. 
Det skal være i punktform. Det handler om investeringer foretaget af {kommune}.
Det hele skal stå på dansk. 
Her er årsagerne:
{årsager}
Hvis der ikke er nogen årsag, så skriv, at der ikke er noget relevant data.
"""

# Generate text based on the dataframe
result = generate_text_from_dataframe(df_prop, api_key, prompt_template, system_prompt)
print(result.content)


##### Tidligere forsøg


# system_prompt = """Du er en assistent, der skal hjælpe en journalist.
#     Lav en opsummering, der først skal beskrive det data,
#     som journalisten sender. Der vil handle om investeringer
#     fra en dansk kommune eller region. I kolonnen
#     'Problematisk ifølge:' fremgår hvilke organisationer,
#     som har sat det angivne selskab på deres eksklusionsliste.
#     Fortæl journalisten hvor mange investeringer, der er problematiske,
#     hvilke beløb, der er problematiske samt totalt investeret,
#     og beskriv overordnet årsager til, at de er problematiske.
#     Lav det som et
#     kort og præcist resumé i en sammenhængende tekst.""" # gerne i punktform.

# system_prompt = """Du er en assistent, der skal hjælpe en journalist.
#     Lav en opsummering, der skal beskrive det problematiske i det data,
#     som journalisten sender. Der vil handle om investeringer
#     fra en dansk kommune eller region. I kolonnen
#     'Problematisk ifølge:' fremgår hvilke organisationer,
#     som har sat det angivne selskab på deres eksklusionsliste.
#     I kolonnen 'Årsag til eksklusion:' står der hvorfor.
#     Lav det som et kort og præcist resumé i punktform,
#     der får de vigtigste informationer med.
#     Beksriv kun data og kom ikke selv med nogle fortolkende input.
#     """  # gerne i punktform.

# Optional prompt template, you can give instructions here
# prompt_template = f"""Opsummer investeringerne foretaget af {kommune}. Her er ekstra information om data.
#                         Der er i alt lavet {antal_inv} investeringer med en total værdi af {round(sum_inv)}.
#                         Der er {round(antal_inv_prop)} problematiske investeringer med en værdi af {sum_inv_prop}.
#                         Skriv et kort resumé med fokus på, hvorfor de er problematiske.
#                     """

# Bornholm = "**Opsummering af investeringer fra Bornholm:**\n\n- **Total antal investeringer:** 1.751\n- **Total værdi af investeringer:** 85.177.238 DKK\n- **Antal problematiske investeringer:** 21\n- **Samlet værdi af problematiske investeringer:** 577.834 DKK\n\n**Overordnede årsager til problematiske investeringer:**\n\n- Investeringerne er problematiske, da de er knyttet til selskaber, som har været involveret i aktiviteter, der strider imod menneskerettigheder eller forårsager omfattende miljøskader.\n- Flere organisationer, herunder *Lærerens Pension* og *FN*, har vurderet, at disse selskaber udviser normbrud ved at ignorere sociale og miljømæssige ansvar.\n\n**Eksempler på problematiske områder:**\n- Levering af tjenester, der understøtter opretholdelsen af bosættelser og transport.\n- Anvendelse af naturressourcer, især vand og land, for kommercielle formål.\n- Overtrædelser af arbejdstagerrettigheder i forbindelse med ILO-konventioner. \n\nBaseret på denne information kan der være grund til at overveje revurdering af investeringerne for at sikre overholdelse af etiske standarder og forvaltning af Bornholm's investeringer."

# Tønder = """**Opsummering af Tønders investeringer:**
# - **Totalt antal investeringer:** 1272
# - **Total værdi af investeringerne:** 224,933,420 DKK
# - **Antal problematiske investeringer:** 19
# - **Total værdi af de problematiske investeringer:** 1,442,457.65 DKK

# **Årsager til problematiske investeringer:**
# - Investerede selskaber er blevet ekskluderet af organisationer som Lærernes Pension og ATP, hvilket indikerer, at de ikke lever op til visse etiske standarder, især relateret til menneskerettigheder og miljømæssige samt sociale forhold.
# - Specifikke årsager til eksklusion inkluderer:
#   - Brud på menneskerettigheder
#   - Involvering i kontroversielle våben
#   - Normovertrædelser ifølge internationale standarder

# Disse problematiske investeringer kan medføre negativ opmærksomhed og potentielle omkostninger for kommunen ifølge principperne for ansvarlig investering og social ansvarlighed."""


# from openai import OpenAI
# client = OpenAI(api_key="sk-KqhGuqSU_xHthzkKSBBu5_pxmue7B4WUqYYRWGSYNAT3BlbkFJosEYrGdoPWc0GorKxY9Kg82CXkAmFmLx1bErEV7JsA")

# completion = client.chat.completions.create(
#     model="gpt-4o-mini",
#     messages=[
#         {"role": "system", "content": "You are a helpful assistant."},
#         {
#             "role": "user",
#             "content": "Write a haiku about recursion in programming."
#         }
#     ]
# )

# print(completion.choices[0].message)
