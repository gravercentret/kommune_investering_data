import pandas as pd

# Load the Excel file into a DataFrame
file_path = '../data/fn_exclude_list.xlsx'  # Replace with your file path
df = pd.read_excel(file_path)

# Mapping letters to their respective meanings
mapping = {
    '(a)': 'The supply of equipment and materials facilitating the construction and the expansion of settlements and the wall, and associated infrastructure',
    '(b)': 'The supply of surveillance and identification equipment for settlements, the wall and checkpoints directly linked with settlements',
    '(c)': 'The supply of equipment for the demolition of housing and property, the destruction of agricultural farms, greenhouses, olive groves and crops',
    '(d)': 'The supply of security services, equipment and materials to enterprises operating in settlements',
    '(e)': 'The provision of services and utilities supporting the maintenance and existence of settlements, including transport',
    '(f)': 'Banking and financial operations helping to develop, expand or maintain settlements and their activities, including loans for housing and the development of businesses',
    '(g)': 'The use of natural resources, in particular water and land, for business purposes',
    '(h)': 'Pollution, and the dumping of waste in or its transfer to Palestinian villages',
    '(i)': 'Captivity of the Palestinian financial and economic markets, as well as practices that disadvantage Palestinian enterprises, including through restrictions on movement, administrative and legal constraints',
    '(j)': 'The use of benefits and reinvestments of enterprises owned totally or partially by settlers for developing, expanding and maintaining the settlements'
}

# Function to translate the letters in "Sub-paragraph of listed activity" into meaningful text
def translate_sub_paragraph(activity):
    if pd.isna(activity):  # Handle blank or NaN values
        return ''
    
    # Split the activity into individual codes and strip spaces
    codes = [code.strip() for code in activity.split(',')]
    
    # Translate each code using the mapping and join them with a semicolon
    translated = '; '.join([mapping.get(code, code) for code in codes])
    
    return translated

# Apply the translation to the DataFrame column
df['Sub-paragraph of listed activity'] = df['Sub-paragraph of listed activity'].apply(translate_sub_paragraph)

# Save the updated DataFrame back to Excel if needed
df.to_excel('../data/fn_exclude_list_new.xlsx' , index=False)  # Replace with desired output path

print("Translation complete and file saved as 'updated_file.xlsx'.")
