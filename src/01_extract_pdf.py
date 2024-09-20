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

# file_save = "../data/Eksklusionslister/ATP_eksklusionsliste.xlsx"
# df.to_excel(file_save, index=False)


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
# file_save = "../data/Eksklusionslister/Nordea_eksklusionsliste.xlsx"
# df.to_excel(file_save, index=False)

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

# file_save = "../data/Eksklusionslister/Lærernes Pension_eksklusionsliste.xlsx"
# df.to_excel(file_save, index=False)

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

# file_save = "../data/Eksklusionslister/AP Pension_eksklusionsliste.xlsx"
# exclusion_data_df.to_excel(file_save, index=False)
# %% Jyske Bank

import pdfplumber
import pandas as pd

# Path to the uploaded PDF file
pdf_path = "../data/Eksklusionslister/Jyske Bank_eksklusionsliste.pdf"

# Open the PDF file with pdfplumber
with pdfplumber.open(pdf_path) as pdf:
    # Extract text from page 2 onwards (since the first page is usually introductory)
    table_data = []
    for page_num in range(1, len(pdf.pages)):
        page = pdf.pages[page_num]
        table = page.extract_table()
        if table:
            table_data.extend(table)  # Add all table rows to the list

# Convert the extracted table data to a DataFrame
df = pd.DataFrame(table_data[1:], columns=table_data[0])  # Use the first row as header

# Clean up the DataFrame (removing empty rows and fixing potential issues)
df.dropna(how="all", inplace=True)  # Remove rows where all columns are NaN
df.columns = ["Selskab", "Kriterie", "Årsag"]  # Set the correct column names

# Create a new column by combining 'Kriterie' and 'Årsag'
df["Årsag til eksklusion"] = df.apply(lambda row: f"{row['Kriterie']} - {row['Årsag']}", axis=1)
df.drop(["Kriterie", "Årsag"], axis=1, inplace=True)
df["Årsag til eksklusion"] = df["Årsag til eksklusion"].str.replace("\n", " ")
df["Årsag til eksklusion"] = df["Årsag til eksklusion"].str.replace("- -", "")

# Save the DataFrame to an Excel file
output_file_path = "../data/Eksklusionslister/Jyske Bank_eksklusionsliste.xlsx"
df.to_excel(output_file_path, index=False)

print(f"Data successfully extracted and saved to {output_file_path}")


# %% Danica Pension & Danske Bank - VIRKER IKKE
import pdfplumber
import pandas as pd

# Path to the uploaded PDF file
pdf_path = "../data/Eksklusionslister/DanskeBank_eksklusionsliste.pdf"


# Function to parse the PDF table and convert it into a DataFrame
def extract_filtered_exclusion_list(pdf_path):
    data = []
    column_names = [
        "Company",
        "Disputed weaponry or arms trade",
        "Biodiversity impacts",
        "Cannabis",
        "Harmful environmental practices",
        "Corruption",
        "Labour practices",
        "Health & Safety issues",
        "Human rights issues",
        "Affiliated with Russia",
        "Product safety",
        "Tax practices",
        "Governance & controls",
    ]

    is_table_started = False  # Track when to start extracting the table
    current_company = None  # Variable to store the current company name

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()

            # Start extracting the table after detecting "Incident & Event-based Screening"
            if "Incident & Event-based Screening" in text:
                is_table_started = True

            # If the table has started, extract it
            if is_table_started:
                table = page.extract_table()
                if table:
                    for row in table:
                        # Filter out rows with all None values or just empty strings
                        cleaned_row = [cell for cell in row if cell is not None and cell.strip()]

                        # Check if the row contains a company name (and assume it’s the first element)
                        if len(cleaned_row) > 1 and not cleaned_row[0].startswith(
                            "X"
                        ):  # Assume it's a company name
                            current_company = cleaned_row[0].strip()
                            x_values = ["X" in col for col in cleaned_row[1:]]
                            # Extend x_values to match the number of columns
                            x_values.extend([False] * (len(column_names) - len(x_values) - 1))
                            data.append([current_company] + x_values)

                        # If the row only contains "X" values (it belongs to the current company), append the X's
                        elif len(cleaned_row) == 1 and cleaned_row[0] == "X":
                            if current_company:
                                x_values = [False] * (
                                    len(column_names) - 1
                                )  # Start with False values
                                x_values[0] = (
                                    True  # Set the first column to True (assuming X refers to the first column)
                                )
                                data[-1][1:] = x_values

    # Create a DataFrame from the data
    df = pd.DataFrame(data, columns=column_names)

    return df


# Extract the data into a DataFrame
df = extract_filtered_exclusion_list(pdf_path)

# Save the DataFrame to an Excel file
df.to_excel("../data/Eksklusionslister/DanskeBank_eksklusionsliste.xlsx", index=False)

print("Data successfully extracted and saved to 'danica_pension_exclusion_list.xlsx'")

# %% LD Fondes
import pdfplumber
import pandas as pd
import re

# Path to the PDF file
pdf_file = "../data/Eksklusionslister/LD Fonde_eksklusionsliste.pdf"

# Create an empty list to store the extracted data
data = []

# Define the expected columns
expected_columns = ["Selskab", "Land", "Selskabstype", "Problematik"]

# List of country exceptions that require special handling
multi_word_countries = ["Saudi Arabien", "Jomfruøerne (britiske)", "Hong Kong"]


def split_row(row_string):
    # Check if the row contains 'Privat' or 'Offentlig'
    if "Privat" in row_string:
        split_at = "Privat"
    elif "Offentlig" in row_string:
        split_at = "Offentlig"
    else:
        return row_string, None, None, None

    # Split the row by 'Privat' or 'Offentlig'
    parts = row_string.split(split_at, 1)
    company_and_country = parts[0].strip()
    company_type = split_at
    problem = parts[1].strip()

    # Find the last word that represents the country
    country_parts = company_and_country.split()

    # Handle special cases for countries
    if country_parts[-1] == "(britiske)":
        country = " ".join(country_parts[-2:])
        company = " ".join(country_parts[:-2])
    elif country_parts[-1] == "Kong":
        country = " ".join(country_parts[-2:])
        company = " ".join(country_parts[:-2])
    elif country_parts[-1] == "Arabien":
        country = " ".join(country_parts[-2:])
        company = " ".join(country_parts[:-2])
    else:
        country = country_parts[-1]
        company = " ".join(country_parts[:-1])

    return company, country, company_type, problem


# Open the PDF file
with pdfplumber.open(pdf_file) as pdf:
    # Loop through all the pages
    for page in pdf.pages:
        # Extract the table
        table = page.extract_table()
        if table:
            for row in table:
                # If row has None values, fix it by splitting at 'Privat' or 'Offentlig'
                if row[1] is None and row[2] is None and row[3] is None:
                    fixed_row = split_row(row[0])
                    data.append(fixed_row)
                else:
                    data.append(row)

# Convert the data into a pandas DataFrame
df = pd.DataFrame(data, columns=expected_columns)

# Drop the first row (index 0)
df = df.drop(0)

# Rename the column 'Problematik' to 'Årsag til eksklusion'
df = df.rename(columns={"Problematik": "Årsag til eksklusion"})

# Save the DataFrame to an Excel file
df.to_excel("../data/Eksklusionslister/LD Fonde_eksklusionsliste.xlsx", index=False)

# print(f"Data extraction complete. Saved to {output_file_path}")

# %% BankInvest

import pdfplumber
import pandas as pd

# Path to the new PDF file
pdf_file = "../data/Eksklusionslister/BankInvest_eksklusionsliste.pdf"

# Create an empty list to store the extracted data
data = []
# Define the expected columns
expected_columns = ["Navn", "Kriterie", "Årsag"]

# List of possible 'Kriterie' values for splitting
kriterie_values = [
    "Product Involvement",
    "Controversial Weapon",
    "Business Ethics",
    "Human Rights",
    "Environment",
    "Labour Rights",
    "Labour Rights, Human Rights",
    "Human Rights, Human Rights",
]


# Function to find where the split should occur based on the 'Kriterie'
def split_at_kriterie(line):
    for kriterie in kriterie_values:
        if kriterie in line:
            # Split the line at the start of the 'Kriterie' value
            parts = line.split(kriterie, 1)
            navn = parts[0].strip()
            årsag = parts[1].strip()  # Last word is 'Årsag'
            return [navn, kriterie, årsag]
    return None


# Open the PDF file
with pdfplumber.open(pdf_file) as pdf:
    # Loop through all the pages
    for page in pdf.pages:
        # Extract the text from the page
        text = page.extract_text()
        lines = text.split("\n")  # Split the text line by line

        # Process each line and extract relevant data
        for line in lines:
            extracted_data = split_at_kriterie(line)
            if extracted_data:
                data.append(extracted_data)

# Convert the data into a pandas DataFrame
df = pd.DataFrame(data, columns=expected_columns)

df["Årsag til eksklusion"] = df.apply(lambda row: f"{row['Kriterie']} - {row['Årsag']}", axis=1)
df.drop(["Kriterie", "Årsag"], axis=1, inplace=True)

display(df)
# Save the DataFrame to an Excel file
df.to_excel("../data/Eksklusionslister/BankInvest_eksklusionsliste.xlsx", index=False)

# print("Table extracted and saved to BankInvest_exclusion_list.xlsx")


# %% Sparinvest - UMULIG

import pdfplumber
import pandas as pd

# Path to the PDF file
pdf_file = "../data/Eksklusionslister/Sparinvest_eksklusionsliste.pdf"

# Create an empty list to store the extracted table data
data = []

# Define the expected columns
expected_columns = ["Selskab", "Baggrund"]

# Open the PDF file
with pdfplumber.open(pdf_file) as pdf:
    # Loop through all the pages
    for page in pdf.pages:
        # Extract the text from the page
        text = page.extract_text()
        print(text)
        lines = text.split("\n")  # Split the text line by line

        # Process each line and extract relevant data
        for line in lines:
            print(line)
            # We assume the company name and background are separated by multiple spaces
            parts = line.split("  ")  # Split based on multiple spaces
            parts = [part.strip() for part in parts if part.strip()]  # Clean up extra spaces
            if len(parts) == 2:  # Ensure we have two parts (Selskab, Baggrund)
                data.append(parts)

# Convert the data into a pandas DataFrame
df = pd.DataFrame(data, columns=expected_columns)
display(df)

# Save the DataFrame to an Excel file
output_path = "../data/Eksklusionslister/Sparinvest_eksklusionsliste.xlsx"
df.to_excel(output_path, index=False)

print(f"Table successfully extracted and saved to {output_path}")


# %% PenSam
import pdfplumber
import pandas as pd


def scrape_pensam_pdf(pdf_file_path, output_file):
    """
    Scrapes the PenSam exclusion list table from a PDF file, adding an 'Årsag til eksklusion' column based on section headers.

    :param pdf_file_path: str, path to the input PDF file
    :param output_file: str, path to the output Excel file
    :return: None
    """
    # Create an empty list to store the extracted data
    data = []
    current_section = None  # This will store the current 'Årsag til eksklusion' (header)

    year_pattern = re.compile(r"^20\d{2}$")

    # Open the PDF file
    with pdfplumber.open(pdf_file_path) as pdf:
        # Loop through all the pages
        for page in pdf.pages:
            # Extract the text from the page
            text = page.extract_text()
            lines = text.split("\n")  # Split the text line by line

            # Process each line
            for line in lines:
                parts = line.split()  # Split the line by whitespace
                if not year_pattern.match(parts[-1]):
                    current_section = line.strip()  # Treat the entire line as the section header
                elif len(parts) >= 3:  # If the line has at least 3 parts (Selskab, Land, Tilføjet)
                    selskab = " ".join(
                        parts[:-2]
                    )  # Everything before the last two parts is the company name
                    land = parts[-2]  # Second last part is 'Land'
                    tilfojet = parts[-1]  # Last part is 'Tilføjet'
                    # Append the row with the current section as the 'Årsag til eksklusion'
                    data.append([selskab, land, tilfojet, current_section])

    # Convert the data into a pandas DataFrame
    df = pd.DataFrame(data, columns=["Selskab", "Land", "Tilføjet", "Årsag til eksklusion"])
    df = df.drop(index=[0, 1])
    # Save the DataFrame to an Excel file
    df.to_excel(output_file, index=False)
    display(df)

    print(f"Data successfully extracted and saved to {output_file}")


# Example usage:
pdf_file = "../data/Eksklusionslister/PenSam_eksklusionsliste.pdf"
output_excel_file = "../data/Eksklusionslister/PenSam_eksklusionsliste.xlsx"
scrape_pensam_pdf(pdf_file, output_excel_file)


# %% Sampension
import pdfplumber
import pandas as pd
import re

# List of exceptions for 'Land' (countries with multiple words)
multi_word_land_two = [
    "South Korea",
    "Saudi Arabien",
    "Hong Kong",
    "Cayman Islands",
    "United Kingdom",
    "New Zealand",
    "South Africa",
    "Faroe Islands",
]

multi_word_land_three = ["Isle of Man", "Virgin Isl (UK)"]

# List of exceptions for 'Årsag' (multiple-word reasons)
multi_word_aarsag = [
    "Atomvåben",
    "Klyngevåben",
    "Menneskerettigheder",
    "Miljø",
    "Landminer",
    "Landeeksklusion",
    "Internationale",
    "Kontroversielle våben",
    "Klima (Kul) / Atomvåben",
    "Klima (Kul)",
    "Arbejdstagerrettigheder",
    "Klima (Tjæresandsolie)",
    "Klima (Metallurgisk Kul)",
    "Klima (Omstilling)",
    "Klima (termisk kul)",
    "Klima(kul)",
    "Klima (tjæresandsolie)",
    "Klima(tjæresandsolie)",
]

pdf_file_path = "../data/Eksklusionslister/Sampension_eksklusionsliste.pdf"

# Create an empty list to store the extracted data
data = []

# Open the PDF file
with pdfplumber.open(pdf_file_path) as pdf:
    # Loop through all the pages
    for page in pdf.pages:
        # Extract the text from the page
        text = page.extract_text()
        lines = text.split("\n")  # Split the text line by line

        for line in lines:
            parts = line.split()  # Split by whitespace
            if not parts:
                continue  # Skip if the line is empty

            parts.pop(0)  # Remove row number

            # Initialize variables for company, cause, and land
            selskab = []
            aarsag = ""
            land = ""

            # Handle land (country)
            if " ".join(parts[-2:]) in multi_word_land_two:
                land = " ".join(parts[-2:])
                del parts[-2:]
            elif " ".join(parts[-3:]) in multi_word_land_three:
                land = " ".join(parts[-3:])
                del parts[-3:]
            else:
                # Special case handling
                if parts[-1] == "sanktionerRussia":
                    land = "Russia"
                    del parts[-1]
                else:
                    land = parts[-1]
                    del parts[-1]

            # Handle company name and cause ('Årsag til eksklusion')
            remains = " ".join(parts)
            for element in multi_word_aarsag:
                if element in remains:
                    selskab_navn, aarsag_match = remains.split(
                        element, 1
                    )  # Split at the first occurrence
                    selskab = selskab_navn.strip()
                    aarsag = element
                    if element == "Internationale":
                        aarsag = "Internationale sanktioner"
                    break

            # Fallback if no specific 'Årsag' found
            if not selskab:
                selskab = remains

            # Append the data as a list of strings, not lists of lists
            data.append([selskab, aarsag, land])

# Convert the data into a pandas DataFrame
df = pd.DataFrame(data, columns=["Selskab", "Årsag til eksklusion", "Land"])
df = df.iloc[1:]
# Print the DataFrame (optional)
print(df)

# output_excel_file = "../data/Eksklusionslister/Sampension_eksklusionsliste.xlsx"
# # # Save the DataFrame to an Excel file
# df.to_excel(output_excel_file, index=False)


# %% Lægernes Pension og Bank
import pdfplumber
import pandas as pd
import re

# Define the path to your PDF file
pdf_file_path = "../data/Eksklusionslister/Lægernes_eksklusionsliste.pdf"

# Initialize an empty list to store the extracted data
country_abr = []
selskab_data = []

# Open the PDF file
with pdfplumber.open(pdf_file_path) as pdf:
    # First pass to extract country abbreviations
    for page in pdf.pages:
        # Extract the text from the page
        text = page.extract_text()
        lines = text.split("\n")  # Split the text line by line
        for line in lines:
            parts = line.split(" ")
            for part in parts:
                # Extract only uppercase country codes with length 2
                if part.isupper() and len(part) == 2 and part.isalpha():
                    if part not in country_abr:
                        country_abr.append(part)

    # Sort and print the country abbreviations
    country_abr.sort()
    print("Extracted Country Abbreviations:", country_abr)

    # Second pass to extract company names and exclusion reasons
    for page in pdf.pages:
        text = page.extract_text()
        lines = text.split("\n")
        for line in lines:
            for element in country_abr:
                # Check if the country abbreviation exists in the line
                if f" {element} " in line:
                    try:
                        # Split the line at the first occurrence of the country abbreviation
                        selskab_navn, aarsag_match = line.split(f" {element} ", 1)
                        # Clean the extracted parts
                        selskab_navn = selskab_navn.strip()
                        aarsag_match = aarsag_match.strip()
                        # Append the results as a tuple to the selskab_data list
                        selskab_data.append((selskab_navn, aarsag_match))
                    except ValueError:
                        # Handle case where splitting fails (e.g., unexpected formatting)
                        pass

# Create a DataFrame with the extracted data
df = pd.DataFrame(selskab_data, columns=["Selskab", "Årsag til eksklusion"])
df = df.sort_values('Selskab')

import pandas as pd

# Assuming your DataFrame 'df' is already loaded with two columns: 'Selskab' and 'Årsag til eksklusion'

# Define the categories and their associated exclusion criteria
category_mapping = {
    'termisk_kul': ['Udvinding af termisk kul', 'Energiproduktion fra termisk kul'],
    'olie_gas_int': ['Integreret olie & gas'],
    'olie_gas_prod': ['Olie & gas udvinding & produktion'],
    'tobak': ['Produktion af tobaksprodukter', 'Distribution af tobaksprodukter', 'Salg af tobaksrelaterede produkter og','services'],
    'atom': ['Atomvåben'],
    'vaaben': ['Kontroversielle våben'],
    'norms': ['Normbrud'],
    'russia': ['Ruslands invasion af Ukraine'],
    'israel': ['Israel/Palestina'],
    'country': ['Landepolitik']
}

# Initialize an empty list to store the sorted data
sorted_data = []

# Loop through each category in the desired order
for category, exclusion_criteria in category_mapping.items():
    # Filter the DataFrame for rows matching the current category's criteria
    df_filtered = df[df['Årsag til eksklusion'].isin(exclusion_criteria)]
    
    # Sort the filtered data alphabetically by the 'Selskab' column
    df_sorted = df_filtered.sort_values(by='Selskab')
    
    # Add the sorted data to the list
    sorted_data.append(df_sorted)

# Concatenate all the sorted data into one DataFrame
df_final = pd.concat(sorted_data)

# Reset the index of the final DataFrame
df_final.reset_index(drop=True, inplace=True)
df['Årsag til eksklusion'].replace(['Salg af tobaksrelaterede produkter og', 'services'], 'Salg af tobaksrelaterede produkter og services')

# Save the DataFrame to an Excel file
# output_file_path = "../data/Eksklusionslister/Lægernes_eksklusionsliste.xlsx"
# df_final.to_excel(output_file_path, index=False)

# print(f"Data extraction complete. Saved to {output_file_path}")



# %% Pædagogernes 

import pdfplumber
import pandas as pd

# Define the path to your PDF file
pdf_path = '../data/Eksklusionslister/Pædagogernes_eksklusionsliste.pdf'



# Lists of countries with multi-word names
multi_word_land_two = [
    "South Korea",
    "Saudi Arabien",
    "Hong Kong",
    "Cayman Islands",
    "United Kingdom",
    "New Zealand",
    "South Africa",
    "Faroe Islands",
]

multi_word_land_three = ["Isle of Man", "Virgin Isl (UK)"]

reasons = ['Antipersonelminer',
    'Arbejdstagerrettigheder',
    'Atomvåben',
    'Fosfor',
    'Klima',
    'Klyngevåben',
    'Menneskerettigheder',
    'Business Model',
    'Tobak',
    'Våbenhandel',
    'Våben',
    'Korruption',
    'Hvid fosfor']

# Flag to start scraping after the header is found
start_scraping = False

# Initialize lists to store the extracted data
isin_list = []
company_list = []
country_list = []
reason_list = []

# Open the PDF file and extract text line by line
with pdfplumber.open(pdf_path) as pdf:
    for page in pdf.pages:
        text = page.extract_text()
        lines = text.split('\n')  # Split the page text by lines
        
        for line in lines:
            # Start scraping after finding the header
            if 'ISIN kode Selskab Land Årsag til eksklusion' in line:
                start_scraping = True
                continue  # Skip the header line

            # Process lines after the header
            if start_scraping:
                # Initialize a list to collect found reasons
                found_reasons = []
                remaining_line = line

                # Check if any reason is present in the line and remove it
                for reason in reasons:
                    if reason in remaining_line:
                        found_reasons.append(reason)
                        remaining_line = remaining_line.replace(reason, "").strip()
                        if remaining_line[-1] == ',':
                            remaining_line = remaining_line.replace(",", "").strip()

                # Join the found reasons into a comma-separated string
                reasons_str = ", ".join(found_reasons)
                reason_list.append(reasons_str)

                # Split the remaining line to extract the ISIN (first part)
                parts = remaining_line.split(" ")
                isin = parts[0]
                isin_list.append(isin)

                # Remove the ISIN from the line and focus on the rest
                remaining_line = " ".join(parts[1:]).strip()

                # Now handle the company and country
                words = remaining_line.split(" ")

                # Check if the last word is in the multi-word country lists
                country = ""
                if len(words) >= 3 and " ".join(words[-3:]) in multi_word_land_three:
                    country = " ".join(words[-3:])
                    company = " ".join(words[:-3]).strip()
                elif len(words) >= 2 and " ".join(words[-2:]) in multi_word_land_two:
                    country = " ".join(words[-2:])
                    company = " ".join(words[:-2]).strip()
                else:
                    country = words[-1]
                    company = " ".join(words[:-1]).strip()

                # Append company and country to their respective lists
                company_list.append(company)
                country_list.append(country)

# Create a DataFrame from the lists
df = pd.DataFrame({
    'ISIN kode': isin_list,
    'Selskab': company_list,
    'Land': country_list,
    'Årsag til eksklusion': reason_list
})

# Save the DataFrame to an Excel file
output_file_path = '../data/Eksklusionslister/Pædagogernes_eksklusionsliste.xlsx'
df.to_excel(output_file_path, index=False)

print(f"Data extraction complete. Saved to {output_file_path}")


# %% Spar Nord

import pdfplumber
import pandas as pd

# Define the path to your PDF file
pdf_path = '../data/Eksklusionslister/Spar Nord_eksklusionsliste.pdf'

# List of exclusion areas (these will appear in the PDF with a number, which we will ignore)
exclusion_areas = [
    "Termisk kul",
    "Oliesand",
    "Arktisk boring",
    "Kontroversielle våben",
    "Internationale normer og konventioner"
]

# Initialize lists to store the extracted data
company_list = []
exclusion_reason_list = []
current_exclusion_reason = None

# Flag to start scraping after the header is found
start_scraping = False

# Open the PDF file and extract text line by line
with pdfplumber.open(pdf_path) as pdf:
    for page in pdf.pages:
        text = page.extract_text()
        lines = text.split('\n')  # Split the page text by lines
        
        for line in lines:
            # Check if the line contains any of the exclusion areas
            for exclusion_area in exclusion_areas:
                if exclusion_area in line:
                    current_exclusion_reason = exclusion_area  # Set the current exclusion reason
                    break  # Move to the next line once the exclusion reason is found
            
            # Check if we are at the "Selskab" header, where the companies start
            if 'Selskab' in line:
                start_scraping = True  # Enable company scraping from this point
                continue  # Skip the header line itself
            
            # If scraping is active, process the company lines
            if start_scraping and current_exclusion_reason:
                if line.strip():  # Ignore empty lines
                    company_name = line.strip()  # The company name is the entire line
                    company_list.append(company_name)
                    exclusion_reason_list.append(current_exclusion_reason)

# Create a DataFrame from the lists
df = pd.DataFrame({
    'Selskab': company_list,
    'Årsag til eksklusion': exclusion_reason_list
})

print(df)
# Save the DataFrame to an Excel file
output_file_path = '../data/Eksklusionslister/Spar Nord_eksklusionsliste.xlsx'
df.to_excel(output_file_path, index=False)

print(f"Data extraction complete. Saved to {output_file_path}")

# %% Industriens Pension
import pdfplumber
import pandas as pd

# Define the path to your PDF file
pdf_path = '../data/Eksklusionslister/Industriens_eksklusionsliste.pdf'


# Lists of countries with multi-word names
multi_word_land_two = [
    "South Korea",
    "Saudi Arabien",
    "Hong Kong",
    "Cayman Islands",
    "United Kingdom",
    "New Zealand",
    "South Africa",
    "Faroe Islands",
    "United States",
]

multi_word_land_three = ["Isle of Man", "Virgin Isl (UK)"]

multi_word_land_four = ['United States of America']

reasons = ['Thermal coal extraction',
    'Labour rights',
    'Cluster Weapons',
    'Oil sands extraction',
    'Human rights',
    'Nuclear Weapons, NPT',
    'Anti-Personnel Mines',
]

# Flag to start scraping after the header is found
start_scraping = False

# Initialize lists to store the extracted data
company_list = []
country_list = []
reason_list = []

# Open the PDF file and extract text line by line
with pdfplumber.open(pdf_path) as pdf:
    for page in pdf.pages:
        text = page.extract_text()
        lines = text.split('\n')  # Split the page text by lines
        
        for line in lines:
            # Start scraping after finding the header
            if 'Company Country Exclusion' in line:
                start_scraping = True
                continue  # Skip the header line

            # Process lines after the header
            if start_scraping:
                # Initialize a list to collect found reasons
                found_reasons = []
                remaining_line = line

                # Check if any reason is present in the line and remove it
                for reason in reasons:
                    if reason in remaining_line:
                        found_reasons.append(reason)
                        remaining_line = remaining_line.replace(reason, "").strip()
                        if remaining_line[-1] == ',':
                            remaining_line = remaining_line.replace(",", "").strip()

                # Join the found reasons into a comma-separated string
                reasons_str = ", ".join(found_reasons)
                reason_list.append(reasons_str)

                # Now handle the company and country
                words = remaining_line.split(" ")

                # Check if the last word is in the multi-word country lists
                country = ""
                if len(words) >= 3 and " ".join(words[-3:]) in multi_word_land_three:
                    country = " ".join(words[-3:])
                    company = " ".join(words[:-3]).strip()
                elif len(words) >= 2 and " ".join(words[-2:]) in multi_word_land_two:
                    country = " ".join(words[-2:])
                    company = " ".join(words[:-2]).strip()
                elif len(words) >= 4 and " ".join(words[-4:]) in multi_word_land_four:
                    country = " ".join(words[-4:])
                    company = " ".join(words[:-4]).strip()
                else:
                    country = words[-1]
                    company = " ".join(words[:-1]).strip()

                # Append company and country to their respective lists
                company_list.append(company)
                country_list.append(country)

# Create a DataFrame from the lists
df = pd.DataFrame({
    'Selskab': company_list,
    'Land': country_list,
    'Årsag til eksklusion': reason_list
})

# Save the DataFrame to an Excel file
output_file_path = '../data/Eksklusionslister/Industriens_eksklusionsliste.xlsx'
df.to_excel(output_file_path, index=False)

print(f"Data extraction complete. Saved to {output_file_path}")



# %%
