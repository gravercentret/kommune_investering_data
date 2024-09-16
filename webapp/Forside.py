import streamlit as st
import pandas as pd
import polars as pl
import matplotlib.pyplot as plt
from utils.data_prep import get_data, get_unique_kommuner, filter_dataframe_by_choice
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

    st.header("Sådan gjorde vi")
    st.markdown(
        """
        Her kan vi have et kort metodeafsnit, og linke til mere.
        """
    )

# Filter dataframe based on user's selection
filtered_df = filter_dataframe_by_choice(st.session_state.df_pl, user_choice)

# Sort first by 'is_problematic' (so that True comes first), then by 'Kommune' and 'ISIN kode' alphabetically
filtered_df = filtered_df.sort(["Problematisk ifølge:", "Kommune", "ISIN kode"], nulls_last=True)


# Write the header
st.header(f'Data for "{user_choice}":')

# Create three columns
col1, col2, col3 = st.columns(3)

# Column 1: Pie chart for "Type" based on "Markedsværdi (DKK)"
with col1:
    # Wrap the content in a container
    with st.container(border=True):
        # Start the box with an opening div
        st.subheader("Fordeling af typer (Markedsværdi)")

        # Group the data by 'Type' and sum the 'Markedsværdi (DKK)' using Polars
        type_distribution = filtered_df.group_by("Type").agg(
            pl.col("Markedsværdi (DKK)").sum().alias("Total Markedsværdi")
        )

        # Convert to pandas for plotting
        type_distribution_pandas = type_distribution.to_pandas()

        # Define a color mapping to ensure consistent colors
        color_mapping = {
            'Aktie': 'lightblue',
            'Obligation': 'lightgreen',
            'Virksomhedsobligation': 'lightcoral',
            'Andet': 'lightgray', 
            'Ikke angivet': 'lightyellow'
        }

        # Match the colors with the values in 'Type'
        colors = [color_mapping.get(type_val, 'gray') for type_val in type_distribution_pandas["Type"]]

        # Plot the pie chart using matplotlib
        fig, ax = plt.subplots()
        wedges, texts, autotexts = ax.pie(
            type_distribution_pandas["Total Markedsværdi"], 
            colors=colors, 
            startangle=90, 
            autopct='%1.1f%%'
        )

        # Add a legend with the 'Type' values
        ax.legend(wedges, type_distribution_pandas["Type"], title="Type", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))

        # Display the pie chart in Streamlit
        st.pyplot(fig)

# Column 2: Number of problematic investments
with col2:
    with st.container(border=True):
        st.subheader("Antal potentielt problematiske investeringer")
        
        # Count the rows where 'Problematisk ifølge:' is not empty
        problematic_count = filtered_df.filter(filtered_df["Problematisk ifølge:"].is_not_null()).shape[0]
        
        # Display the number
        st.metric(label="Antal", value=problematic_count)

# Column 3: Key financial figures ('Nøgletal')
with col3:
    with st.container(border=True):
        st.subheader("Nøgletal")
        
        # Calculate key numbers like the total sum of 'Markedsværdi (DKK)' and other statistics
        total_markedsvaerdi = filtered_df.select(pl.sum("Markedsværdi (DKK)")).to_pandas().iloc[0, 0]
        
        # Display key numbers
        st.write(f"**Total Markedsværdi (DKK):** {total_markedsvaerdi:,.2f}")
        # Add more key figures as necessary, e.g., mean, median, etc.
        #st.write(f"**Gennemsnitlig Markedsværdi (DKK):** {filtered_df['Markedsværdi (DKK)'].mean():,.2f}")
        #st.write(f"**Median Markedsværdi (DKK):** {filtered_df['Markedsværdi (DKK)'].median():,.2f}")

# Convert to Pandas for displaying in Streamlit
filtered_df = filtered_df.to_pandas()

# Apply the color_rows_limited function to the top 1000 rows
# filtered_df = filtered_df.style.apply(lambda row: color_rows_limited(row, row.name), axis=1)
def color_one_column(val):
    color = 'red' if val != None else ''
    return f'background-color: {color}'

# Display the dataframe below the three columns
st.dataframe(filtered_df.style.map(color_one_column, subset=['Problematisk ifølge:']))


