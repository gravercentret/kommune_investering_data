import streamlit as st
import pandas as pd
import polars as pl
import numpy as np
import re
from io import BytesIO
import matplotlib.pyplot as plt
from utils.data_prep import (
    get_data,
    get_unique_kommuner,
    filter_dataframe_by_choice,
    generate_organization_links,
    filter_df_by_search,
    fix_column_types,
)
from utils.styling import color_rows_limited
from src.config import set_pandas_options, set_streamlit_options

# Apply the settings
set_pandas_options()
set_streamlit_options()

# Function to load and inject CSS into the Streamlit app
# def load_css(file_name):
#     with open(file_name) as f:
# st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# load_css("webapp/style.css")

# st.markdown(f"""
#     <style>
#     /* Change the background color of the main container */
#     .main {{
#         background-color: #ffffff;
#     }}

#     /* Customize the font and text color for better readability */
#     h1, h2, h3, h4, h5, h6, p {{
#         color: #333; /* Darker text color for better contrast */
#         font-family: Arial, sans-serif; /* Choose your preferred font */
#     }}
#     </style>
# """, unsafe_allow_html=True)

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
    user_choice = st.selectbox(
        "Vælg område:",
        dropdown_options,
        help="Skriv i boksen for at søge efter bestemt kommune/region.",
        placeholder="Vælg en kommune/region.",
    )

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
    type_distribution = (
        filtered_df.group_by("Type")
        .agg(pl.col("Markedsværdi (DKK)").sum().alias("Total Markedsværdi"))
        .to_pandas()
    )  # Convert to pandas for plotting

    # Drop rows with missing values (NaN) in 'Total Markedsværdi' or 'Type'
    type_distribution = type_distribution.dropna(subset=["Total Markedsværdi", "Type"])

    # Combine 'Andet' and 'Ikke angivet' into one category
    type_distribution["Type"] = type_distribution["Type"].replace(
        {"Andet": "Andet/Ikke angivet", "Ikke angivet": "Andet/Ikke angivet"}
    )

    # Re-aggregate the data to group by the combined category, summing only the numeric column
    type_distribution = type_distribution.groupby("Type", as_index=False)[
        "Total Markedsværdi"
    ].sum()

    # Define a color mapping for consistent colors
    color_mapping = {
        "Aktie": "cornflowerblue",
        "Obligation": "lightgreen",
        "Virksomhedsobligation": "lightblue",
        "Andet/Ikke angivet": "lightgray",
    }

    # Match the colors with the values in 'Type'
    colors = [color_mapping.get(type_val, "gray") for type_val in type_distribution["Type"]]

    # Plot the pie chart using matplotlib
    fig, ax = plt.subplots()
    ax.pie(
        type_distribution["Total Markedsværdi"],
        colors=colors,
        startangle=0,
        autopct="%1.1f%%",
        textprops={"fontsize": 14},
    )

    # Add a legend with the 'Type' values
    ax.legend(
        type_distribution["Type"], title="Type", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1)
    )

    # Display the pie chart in Streamlit
    st.pyplot(fig)


# Column 2: Number of problematic investments
with col2:
    with st.container(border=True):
        col2_1, col2_2, col2_3 = st.columns(3)

        with col2_1:
            with st.container(border=True):
                st.markdown("***Antal investeringer udpeget som problematiske:***")

                # Count the rows where 'Problematisk ifølge:' is not empty
                problematic_count = filtered_df.filter(
                    filtered_df["Problematisk ifølge:"].is_not_null()
                ).shape[0]

                # Display the number in red
                st.markdown(
                    f'<h1 style="color:red;">{problematic_count}</h1>', unsafe_allow_html=True
                )
        with col2_2:
            with st.container(border=True):
                st.markdown("***Antal investeringer fra ekskluderede lande:***")

                # Display the second number in yellow
                st.markdown(
                    f'<h1 style="color:orange;">{problematic_count + 4}</h1>',
                    unsafe_allow_html=True,
                )
        with col2_3:
            with st.container(border=True):
                st.markdown("***Antal investeringer værd at undersøge nærmere:***")

                # Display the second number in yellow
                st.markdown(
                    f'<h1 style="color:yellow;">{problematic_count + 100}</h1>',
                    unsafe_allow_html=True,
                )
    # Nøgletal
    with st.container(border=True):
        st.subheader("Nøgletal")

        # Calculate the total number of investments
        antal_inv = len(filtered_df)
        st.write(f"**Antal investeringer:** {antal_inv}")

        # Calculate the total sum of 'Markedsværdi (DKK)' and display it in both DKK and millions
        total_markedsvaerdi = (
            filtered_df.select(pl.sum("Markedsværdi (DKK)")).to_pandas().iloc[0, 0]
        )
        markedsvaerdi_million = total_markedsvaerdi / 1_000_000
        st.write(
            f"**Total Markedsværdi (DKK):** {total_markedsvaerdi:,.2f} ({markedsvaerdi_million:,.1f} millioner)"
        )

        # Filter for problematic investments and calculate the total sum of their 'Markedsværdi (DKK)'
        prob_df = filtered_df.filter(filtered_df["Problematisk ifølge:"].is_not_null())
        prob_markedsvaerdi = prob_df.select(pl.sum("Markedsværdi (DKK)")).to_pandas().iloc[0, 0]
        prob_markedsvaerdi_million = prob_markedsvaerdi / 1_000_000
        st.write(
            f"**Markedsværdi af problematiske investeringer:** {prob_markedsvaerdi:,.2f} ({prob_markedsvaerdi_million:,.1f} millioner)"
        )


# Display the dataframe below the three columns
# st.dataframe(filtered_df.style.map(color_one_column, subset=['Problematisk ifølge:']))
# [['Kommune', 'Udsteder', 'Markedsværdi (DKK)', 'Type', 'Problematisk ifølge:', 'Årsag til eksklusion']]
st.dataframe(
    filtered_df[
        [
            "OBS",
            "Kommune",
            "Udsteder",
            "Markedsværdi (DKK)",
            "Type",
            "Problematisk ifølge:",
            "Årsag til eksklusion",
        ]
    ],
    column_config={
        "Kommune": "Kommune",
        "Udsteder": st.column_config.TextColumn(width="medium"),
        "Markedsværdi (DKK)": st.column_config.NumberColumn(format="%.2f"),
        "Type": "Type",
        "Problematisk ifølge:": st.column_config.TextColumn(width="medium"),
        "Årsag til eksklusion": st.column_config.TextColumn(width="large"),
    },
    hide_index=True,
)

# Call the function to display relevant links based on the 'Problematisk ifølge:' column
generate_organization_links(filtered_df, "Problematisk ifølge:")


# Function to convert dataframe to Excel and create a downloadable file
def to_excel(filtered_df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
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
    file_name=f"Investeringer for {user_choice}{search_query}.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
)
# st.markdown("Bornholm har foretaget et bredt spektrum af investeringer, der spænder over forskellige typer værdipapirer, herunder aktier og obligationer. Nedenfor er en opsummering af de vigtigste data:\n\n### Oversigt over investeringerne:\n- **Antal diverse investeringer:** 1755\n- **Type:** Overvejende aktier og obligationer, med en præsentation tilknyttet forskellige virksomheder og statslige organisationer.\n\n### Kategori for investeringerne:\n- Aktier: Stort fokus på aktier i virksomheder som **Coca-Cola HBC AG**, **Nestlé S.A.**, og **Volksbank Wien AG**.\n- Obligationer: Investeringer i forskellige statsobligationer, også fra danske udstedere som **Realkredit Danmark** og **Nykredit**.\n\n### Markedsværdi:\n- **Total markedsværdi:** Varieret, med nogle investeringer med en betydelig individuel værdi, f.eks. obligationer fra **Erste Group Bank AG** og aktier i **Novozymes**.\n\n### Problematisk investering:\n- Flere af investeringerne er erklæret problematiske ifølge visse investeringsprincipper og etiske retningslinjer. Dette drejer sig ofte om investeringer i virksomheder, der er involveret i kontroversielle aktiviteter, som for eksempel produktion af våben.\n\n### Udelukkelseskriterier:\n- Der er anvendt kriterier omkring menneskerettigheder og miljømæssige normer, specielt hvad angår investeringer, der involverer våbenproduktion og virksomheder uden klart ansvar over for sociale og miljømæssige virkninger.\n\n### Samlet indtryk:\nBornholms investeringsstrategi viser en veldiversificeret portefølje med stærk tilstedeværelse i både aktier og obligationer, men også en opmærksomhed på etiske standarder og bæredygtighed. Det er væsentligt at bemærke, at der er en aktiv vurdering af de etiske konsekvenser af investeringerne, hvilket reflekterer en ansvarlig investeringspraksis.")

# st.markdown("Her er en opsummering af investeringsdata for Bornholm:\n\n- **Antal problematiske investeringer**: 2 \n- **Samlet problematiske beløb**: 86.114.982,7 DKK\n- **Total investeret beløb**: 1.687.896.626,05 DKK\n- **Problematisk ifølge organisationer**: Lærerens Pension, ATP\n- **Årsager til investeringerne**:\n  - Lærerens Pension: **Kontroversielle våben**\n  - ATP: **Brud på menneskerettigheder** og normer i forbindelse med eksklusion.\n\nOverordnet set stammer problemerne fra manglende overholdelse af menneskerettighederne og forbindelser til kontroversielle våben i disse investeringer.")
