# %% Velliv

import pdfplumber
import pandas as pd

# Path to the uploaded file
# pdf_path = "../data/Eksklusionslister/Velliv_eksklusionsliste.pdf"

# Define the list of keywords for 'kommentar'
keywords = [
    "Controversiel weapons",
    "Fossil - Arctic",
    "Fossil - Coal expansion",
    "Fossil - Fracking",
    "Fossil - Oil sand",
    "Fossil - Thermal coal",
    "Fossil - Transition",
    "Norm violation>Business Ethics",
    "Norm violation>Environment",
    "Norm violation>Human Rights",
    "Normviolation>Human Rights",
    "Tobacco",
]

# Initialize an empty list to store the rows
data = []

with pdfplumber.open(pdf_path) as pdf:
    for page in pdf.pages:
        text = page.extract_text()
        lines = text.split("\n")
        for line in lines:
            for keyword in keywords:
                if keyword in line:
                    # Split the line into the part before the keyword and the keyword itself
                    company_part = line.replace(
                        keyword, ""
                    ).strip()  # The company name and rest of the line
                    kommentar_part = keyword  # The keyword itself

                    # Append the company name and the keyword to the data list
                    data.append([company_part, kommentar_part])
                    break  # Once a keyword is found, skip checking other keywords for this line

# Convert the data list to a pandas DataFrame
df = pd.DataFrame(data, columns=["Selskab", "Årsag til eksklusion"])

print(df)

file_save = "../data/Eksklusionslister/Velliv_eksklusionsliste.xlsx"
df.to_excel(file_save, index=False)

# %% ATP - Get Keywords
import pdfplumber
import re

# Path to the uploaded PDF file
pdf_path = "../data/Eksklusionslister/ATP_eksklusionsliste.pdf"


# Function to find all unique keywords
def extract_keywords_from_pdf(pdf_path):
    keywords = set()  # Use a set to avoid duplicates
    year_pattern = re.compile(r"\b(19|20)\d{2}\b")  # Regex pattern to find years (e.g., 2019, 2020)

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            lines = text.split("\n")
            for line in lines:
                match = year_pattern.search(line)
                if match:
                    # Find the position of the year and extract the part before it
                    year = match.group(0)
                    before_year = line[
                        : line.index(year)
                    ].strip()  # Extract the text before the year
                    words = before_year.split()  # Split into words

                    if words:  # Make sure there's something before the year
                        # Take the last word(s) as the keyword (you can tweak this if necessary)
                        keyword = " ".join(
                            words[-1:]
                        )  # Attempt to capture two words in case of phrases
                        keywords.add(keyword)

    return list(keywords)  # Convert the set to a list


# Extract and display the keywords
unique_keywords = extract_keywords_from_pdf(pdf_path)

# Display the result (list of unique keywords)
print(unique_keywords)

# %%
import pdfplumber
import re
import pandas as pd

# Path to the uploaded PDF file
pdf_path = "../data/Eksklusionslister/ATP_eksklusionsliste.pdf"

keywords = [
    "Menneskerettigheder",
    "Klyngebomber",
    "Sikkerhedsforhold",
    "Korruption",
    "Brud på NPT",
    "Biodiversitet",
    "ILO-brud",
    "Antipersonelle miner",
    "Klyngebomber/brud på NPT",
    "Klyngebomber/antipersonelle miner",
]


# Function to extract company name, exclusion reason, and year
def extract_data_from_pdf(pdf_path, keywords):
    data = []  # List to store the rows
    year_pattern = re.compile(r"\b(19|20)\d{2}\b")  # Regex pattern to find years

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            lines = text.split("\n")
            for line in lines:
                # Check if the line contains any of the keywords
                for keyword in keywords:
                    if keyword in line:
                        match = year_pattern.search(line)
                        if match:
                            year = match.group(0)  # Extract the year
                            # Split the line into parts
                            parts = line.split(keyword)
                            company = parts[0].strip()  # Company name (before the keyword)
                            exclusion_reason = keyword  # Årsag til eksklusion
                            data.append([company, exclusion_reason, year])  # Add to the list
                        break  # No need to check other keywords for this line

    return data


# Extract the data
extracted_data = extract_data_from_pdf(pdf_path, keywords)

# Convert the data list into a pandas DataFrame
df = pd.DataFrame(extracted_data, columns=["Selskab", "Årsag til eksklusion", "Årstal"])

print(df)

file_save = "../data/Eksklusionslister/ATP_eksklusionsliste.xlsx"
df.to_excel(file_save, index=False)


# %%

import pdfplumber

# Path to the uploaded PDF file
pdf_path = "../data/Eksklusionslister/Nordea_eksklusionsliste.pdf"


# Function to extract keywords after "Involvement" or "Violation"
def extract_keywords_after_phrases(pdf_path):
    keywords = set()  # Use a set to avoid duplicates
    phrases = ["Involvement", "Violation"]  # The words we are looking for

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            lines = text.split("\n")
            for line in lines:
                # Check if the line contains "Involvement" or "Violation"
                for phrase in phrases:
                    if phrase in line:
                        # Extract the part after the phrase
                        keyword = line[
                            line.index(phrase) :
                        ].strip()  # Keep the phrase and everything after it
                        keywords.add(keyword)  # Add the extracted comment to the set
                        break  # Stop checking other phrases once we found a match

    return list(keywords)  # Convert the set to a list


# Extract the keywords
extracted_keywords = extract_keywords_after_phrases(pdf_path)

# Display the list of extracted keywords
print(extracted_keywords)

# %%
import pdfplumber

# Path to the uploaded PDF file
pdf_path = "../data/Eksklusionslister/Nordea_eksklusionsliste.pdf"

keywords = [
    "Involvement in depleted uranium ammunition &",
    "Involvement in anti-personnel mines",
    "Involvement in pornography",
    "Violation of human rights related norms",
    "Involvement in nuclear weapons",
    "Involvement in Arctic drilling",
    "Involvement in coal mining",
    "Involvement in cluster munitions & anti-personnel",
    "Involvement in depleted uranium ammunition",
    "Involvement in cluster munitions",
    "Violation of established norms",
    "Violation of international norms",
    "Involvement in oil sand",
    "Involvement in cluster munitions & nuclear weapons",
    "Arms export to Myanmar",
    "Operation in Myanmar and Russia",
    "Norms violation of indigenous peoples rights",
    "GHG Emission",
    "Norms violation associated to environmental pollution",
    "Russia's & Belarus' unprovoked aggression in the",
    "war in Ukraine",
    "and failure to up-hold health and safety standards",
]

# Initialize an empty list to store the rows
data = []

with pdfplumber.open(pdf_path) as pdf:
    for page in pdf.pages:
        text = page.extract_text()
        lines = text.split("\n")
        for line in lines:
            for keyword in keywords:
                if keyword in line:
                    # Split the line into the part before the keyword and the keyword itself
                    company_part = line.replace(
                        keyword, ""
                    ).strip()  # The company name and rest of the line
                    kommentar_part = keyword  # The keyword itself

                    # Append the company name and the keyword to the data list
                    data.append([company_part, kommentar_part])
                    break  # Once a keyword is found, skip checking other keywords for this line


# Convert the data list to a pandas DataFrame
df = pd.DataFrame(data, columns=["Selskab", "Gammel Årsag til eksklusion"])

print(df)

# %%
import difflib
import pandas as pd

# List of correct keywords
correct_keywords = [
    "Involvement in depleted uranium ammunition & nuclear weapons",
    "Involvement in anti-personnel mines",
    "Involvement in pornography",
    "Violation of human rights related norms",
    "Involvement in nuclear weapons",
    "Involvement in Arctic drilling",
    "Involvement in coal mining",
    "Involvement in cluster munitions & anti-personnel mines",
    "Involvement in depleted uranium ammunition",
    "Involvement in cluster munitions",
    "Violation of established norms",
    "Violation of international norms",
    "Involvement in oil sand",
    "Involvement in cluster munitions & nuclear weapons",
    "Arms export to Myanmar",
    "Operation in Myanmar and Russia",
    "Norms violation of indigenous peoples rights",
    "GHG Emission",
    "Norms violation associated to environmental pollution and failure to up-hold health and safety standards",
    "Russia's & Belarus' unprovoked aggression in the war in Ukraine",
]

# Example DataFrame with partial or incorrect keywords in 'Årsag til eksklusion'
# df['Gammel Årsag til eksklusion'] = df['Årsag til eksklusion']


# Function to match partial keyword with the closest correct keyword
def correct_keyword(partial_keyword, correct_keywords):
    # Find the closest match for the partial keyword
    matches = difflib.get_close_matches(partial_keyword, correct_keywords, n=1, cutoff=0.6)
    # If a match is found, return the closest one; otherwise, return the original keyword
    return matches[0] if matches else partial_keyword


# Apply the correction to the 'Årsag til eksklusion' column
df["Årsag til eksklusion"] = df["Gammel Årsag til eksklusion"].apply(
    lambda x: correct_keyword(x, correct_keywords)
)

df.drop(columns="Gammel Årsag til eksklusion", inplace=True)
df["Selskab"].dropna(inplace=True)

print(df)

## Virksomheder på to linjer er ikke korrekt, manuelt rettes
file_save = "../data/Eksklusionslister/Nordea_eksklusionsliste.xlsx"
df.to_excel(file_save, index=False)

# %% Lærernes Pension
import pdfplumber
import pandas as pd

# Path to the uploaded PDF file
# pdf_path = "../data/Eksklusionslister/Lærernes Pension_eksklusionsliste.pdf"


# Function to parse the PDF table and convert it into a DataFrame
def extract_filtered_exclusion_list(pdf_path):
    data = []
    column_names = [
        "Name",
        "Norms",
        "Controversial Weapons",
        "Weapons and Military",
        "Tobacco",
        "Fossils",
    ]

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            table = page.extract_table()
            if table:
                for row in table[1:]:  # Skip the first line (header row)
                    name = row[0].strip()  # Company name
                    norms = True if row[1].strip().lower() == "x" else False
                    controversial_weapons = True if row[2].strip().lower() == "x" else False
                    weapons_military = True if row[3].strip().lower() == "x" else False
                    tobacco = True if row[4].strip().lower() == "x" else False
                    fossils = True if row[5].strip().lower() == "x" else False

                    # Append the row only if at least one of the columns has True
                    if norms or controversial_weapons or weapons_military or tobacco or fossils:
                        data.append(
                            [name, norms, controversial_weapons, weapons_military, tobacco, fossils]
                        )

    # Create a DataFrame from the data
    df = pd.DataFrame(data, columns=column_names)

    return df


# Call the function to extract data and create the DataFrame
exclusion_df = extract_filtered_exclusion_list(pdf_path)

# %%


# Function to generate the new DataFrame with Selskab and Årsag til
#  columns
def create_exclusion_reasons_df(df):
    exclusion_columns = [
        "Norms",
        "Controversial Weapons",
        "Weapons and Military",
        "Tobacco",
        "Fossils",
    ]

    # Create an empty list to store the new rows
    new_data = []

    for _, row in df.iterrows():
        # Extract the company name
        company_name = row["Name"]

        # Create a list of reasons for exclusion by checking True values in the relevant columns
        reasons = [col for col in exclusion_columns if row[col]]

        # Join the reasons into a single string
        reasons_str = ", ".join(reasons) if reasons else "No Exclusion"

        # Append the company name and reasons to the new data list
        new_data.append([company_name, reasons_str])

    # Create a new DataFrame with the updated structure
    new_df = pd.DataFrame(new_data, columns=["Selskab", "Årsag til eksklusion"])

    return new_df


df = create_exclusion_reasons_df(exclusion_df)
print(df)

file_save = "../data/Eksklusionslister/Lærernes Pension_eksklusionsliste.xlsx"
df.to_excel(file_save, index=False)

# %% AP Pension

import pdfplumber
import pandas as pd
import re

# Path to the uploaded PDF file
pdf_path = "../data/Eksklusionslister/AP Pension_eksklusionsliste.pdf"

# List of all areas (reasons for exclusion) in lower case for case-insensitive matching
exclusion_areas = [
    "kontroversielle våben",
    "klimarelaterede forhold",
    "tobak",
    "menneskerettigheder",
    "selskabsledelse",
    "lande",
]


def extract_exclusion_data(pdf_path, exclusion_areas):
    data = []  # To store the extracted data
    current_reason = None
    collecting_companies = False  # Flag to start collecting company names
    section_title_count = {}  # To track how many times a section title has appeared

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            lines = text.split("\n")

            for idx, line in enumerate(lines):
                line_stripped = line.strip()
                line_lower = line_stripped.lower()

                # Check if the line exactly matches any of the exclusion areas
                if line_lower in exclusion_areas:
                    current_reason = line_stripped  # Use the original line for current_reason
                    # Update the count for this section title
                    section_title_count[current_reason] = (
                        section_title_count.get(current_reason, 0) + 1
                    )

                    # Start collecting companies after the second occurrence of the section title
                    if section_title_count[current_reason] >= 2:
                        collecting_companies = True
                    else:
                        collecting_companies = False
                    continue  # Move to the next line

                # If we're collecting companies
                if collecting_companies:
                    # Check if the line is another section title
                    if line_lower in exclusion_areas:
                        current_reason = line_stripped
                        # Reset the counter and flags for the new section
                        section_title_count[current_reason] = 1
                        collecting_companies = False
                        continue
                    # Skip page numbers or lines that match 'side x/y'
                    elif re.match(r"^side \d+/\d+$", line_lower):
                        continue
                    # Collect non-empty lines as company names
                    elif line_stripped != "":
                        company_name = line_stripped
                        data.append([company_name, current_reason])
                    else:
                        continue  # Skip empty lines

    # Create a DataFrame from the collected data
    df = pd.DataFrame(data, columns=["Selskab", "Årsag til eksklusion"])

    return df


# Call the function to extract the data from the PDF
exclusion_data_df = extract_exclusion_data(pdf_path, exclusion_areas)

# Print the DataFrame
print(exclusion_data_df)

file_save = "../data/Eksklusionslister/AP Pension_eksklusionsliste.xlsx"
exclusion_data_df.to_excel(file_save, index=False)
# %%
