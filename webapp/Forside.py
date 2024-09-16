import streamlit as st
import pandas as pd
import polars as pl
import numpy as np
import re
from io import BytesIO
import matplotlib.pyplot as plt
from utils.data_prep import get_data, get_unique_kommuner, filter_dataframe_by_choice, generate_organization_links, filter_df_by_search, fix_column_types
from utils.styling import color_rows_limited
from src.config import set_pandas_options, set_streamlit_options

# Apply the settings
set_pandas_options()
set_streamlit_options()

if "df_pl" not in st.session_state:
    st.session_state.df_pl = get_data()

# Title of the app
st.title("Investeringer")

# Get unique municipalities and sort alphabetically
unique_kommuner = get_unique_kommuner(st.session_state.df_pl)

# Define custom categories
all_values = "Hele landet"
municipalities = "Alle kommuner"
regions = "Alle regioner"

# Create dropdown options
dropdown_options = [all_values, municipalities, regions] + unique_kommuner

# Sidebar with selection options
with st.sidebar:
    user_choice = st.selectbox("Vælg område:", dropdown_options, help="Skriv i boksen for at søge efter bestemt kommune/region.", placeholder='Vælg en kommune/region.')

    search_query = st.text_input("Søg i tabellen:", "")

    st.header("Sådan gjorde vi")
    st.markdown(
        """
        Her kan vi have et kort metodeafsnit, og linke til mere.
        """
    )

# Filter dataframe based on user's selection
filtered_df = filter_dataframe_by_choice(st.session_state.df_pl, user_choice)

filtered_df = filter_df_by_search(filtered_df, search_query)

filtered_df = fix_column_types(filtered_df)

# Sort first by 'is_problematic' (so that True comes first), then by 'Kommune' and 'ISIN kode' alphabetically
filtered_df = filtered_df.sort(["Problematisk ifølge:", "Kommune", "ISIN kode"], nulls_last=True)

# Conditionally display the header based on whether a search query is provided
if search_query:
    st.header(f'Data for "{user_choice}" og "{search_query}":')
else:
    st.header(f'Data for "{user_choice}":')

# Create three columns
col1, col2 = st.columns([0.4, 0.6])

# Assuming filtered_df is your Polars dataframe that has been filtered already
# Column 1: Pie chart for "Type" based on "Markedsværdi (DKK)"
with col1:
    st.subheader("Fordeling af typer (Markedsværdi)")

    # Group the data by 'Type' and sum the 'Markedsværdi (DKK)'
    type_distribution = filtered_df.group_by("Type").agg(
        pl.col("Markedsværdi (DKK)").sum().alias("Total Markedsværdi")
    ).to_pandas()  # Convert to pandas for plotting

    # Drop rows with missing values (NaN) in 'Total Markedsværdi' or 'Type'
    type_distribution = type_distribution.dropna(subset=["Total Markedsværdi", "Type"])

    # Combine 'Andet' and 'Ikke angivet' into one category
    type_distribution["Type"] = type_distribution["Type"].replace({
        'Andet': 'Andet/Ikke angivet', 
        'Ikke angivet': 'Andet/Ikke angivet'
    })

    # Re-aggregate the data to group by the combined category, summing only the numeric column
    type_distribution = type_distribution.groupby("Type", as_index=False)["Total Markedsværdi"].sum()

    # Define a color mapping for consistent colors
    color_mapping = {
        'Aktie': 'cornflowerblue',
        'Obligation': 'lightgreen',
        'Virksomhedsobligation': 'lightblue',
        'Andet/Ikke angivet': 'lightgray'
    }

    # Match the colors with the values in 'Type'
    colors = [color_mapping.get(type_val, 'gray') for type_val in type_distribution["Type"]]

    # Plot the pie chart using matplotlib
    fig, ax = plt.subplots()
    ax.pie(
        type_distribution["Total Markedsværdi"], 
        colors=colors, 
        startangle=0, 
        autopct='%1.1f%%',
        textprops={'fontsize': 14}
    )

    # Add a legend with the 'Type' values
    ax.legend(type_distribution["Type"], title="Type", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))

    # Display the pie chart in Streamlit
    st.pyplot(fig)


# Column 2: Number of problematic investments
with col2:
    with st.container(border=True):
        st.subheader("Antal investeringer udpeget som problematiske:")
        
        # Count the rows where 'Problematisk ifølge:' is not empty
        problematic_count = filtered_df.filter(filtered_df["Problematisk ifølge:"].is_not_null()).shape[0]
        
        # Display the number in red
        st.markdown(f'<h1 style="color:red;">{problematic_count}</h1>', unsafe_allow_html=True)

        st.subheader("Antal investeringer værd at undersøge nærmere:")

        # Display the second number in yellow
        st.markdown(f'<h1 style="color:orange;">{problematic_count + 4}</h1>', unsafe_allow_html=True)

# # Column 3: Key financial figures ('Nøgletal')
# with col3:
    with st.container(border=True):
        st.subheader("Nøgletal")
        
        # Calculate key numbers like the total sum of 'Markedsværdi (DKK)' and other statistics
        total_markedsvaerdi = filtered_df.select(pl.sum("Markedsværdi (DKK)")).to_pandas().iloc[0, 0]

        # Calculate the value in millions
        markedsvaerdi_million = total_markedsvaerdi / 1_000_000

        # Display the total value and the value in millions
        st.write(f"**Total Markedsværdi (DKK):** {total_markedsvaerdi:,.2f} ({markedsvaerdi_million:,.1f} millioner)")

# # Convert to Pandas for displaying in Streamlit
# df = filtered_df.to_pandas()
# df.index = np.arange(1, len(df) + 1)

# ### Fritekstsøgning
# Free text search input
# search_query = st.text_input("Søg i tabellen:", "")

# df = filtered_df

# # Use case-insensitive search if query is provided
# if search_query:
#     # Create a case-insensitive regex search pattern
#     search_pattern = f"(?i){search_query}"

#     # Replace NA values with empty strings and cast columns to string
#     df = df.with_columns([pl.col(col).fill_null("").cast(str) for col in df.columns])

#     # Combine conditions across all columns using logical OR (|) operator
#     filter_expr = None
#     for col in df.columns:
#         condition = pl.col(col).str.contains(search_pattern)
#         filter_expr = condition if filter_expr is None else filter_expr | condition

#     # Apply the filter
#     filtered_df = df.filter(filter_expr)
# else:
#     filtered_df = df

# Apply the color_rows_limited function to the top 1000 rows
# filtered_df = filtered_df.style.apply(lambda row: color_rows_limited(row, row.name), axis=1)
def color_one_column(val):
    color = 'red' if val != None else ''
    return f'background-color: {color}'

# Display the dataframe below the three columns
# st.dataframe(filtered_df.style.map(color_one_column, subset=['Problematisk ifølge:']))
st.dataframe(filtered_df)

# Call the function to display relevant links based on the 'Problematisk ifølge:' column
generate_organization_links(filtered_df, "Problematisk ifølge:")

# Function to convert dataframe to Excel and create a downloadable file
def to_excel(filtered_df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        filtered_df.to_excel(writer, index=False)
    processed_data = output.getvalue()
    return processed_data

filtered_df = filtered_df.to_pandas()
# Convert dataframe to Excel
excel_data = to_excel(filtered_df)

# Create a download button
st.download_button(
    label="Download til Excel",
    data=excel_data,
    file_name=f'Investeringer for {user_choice} og {search_query}.xlsx',
    mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
)
