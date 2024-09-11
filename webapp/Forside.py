import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
from utils.data_prep import data_processing, data_split_kom_reg

# Load and process data
# path = "data/data_investeringer.xlsx"
# df = pd.read_excel(path)
# df = data_processing(df)
# df_reg, df_kom = data_split_kom_reg(df)

# Create an SQLite engine
engine = create_engine(
    "sqlite:///C:/Users/Anja/Documents/Python_projekter/kommune_investering/src/investerings_database.db"
)

# Example of a query to retrieve data from the local SQLite database
# Connect to the SQLite database
with engine.connect() as conn:
    # Sample query to select all rows
    query = """
        SELECT [Kommune], [ISIN kode], [Værdipapirets navn], 
        [Udsteder], [Markedsværdi (DKK)], [Type], 
        [Problematisk ifølge (FN)], 
        [Problematisk ifølge (pensionsselskab)], 
        [Årsag til eksklusion] 
        FROM kommunale_regioner_investeringer;
    """

    # Execute the query and load the result into a new DataFrame
    df = pd.read_sql(query, conn)

# Streamlit App
# Set the page layout to wide
st.set_page_config(layout="wide")

# Title of the app
st.title("Titel")

# Create a dropdown in the sidebar for selecting a "Kommune" value
selected_kommune = st.sidebar.selectbox("Select a Kommune:", df["Kommune"].dropna().unique())

# Filter the dataframe based on the selected "Kommune"
filtered_df = df[df["Kommune"] == selected_kommune]

# Display the filtered dataframe
st.write("Kommune data:")
st.dataframe(filtered_df)

# Display basic information
total_rows = filtered_df.shape[0]
total_markedsværdi = filtered_df["Markedsværdi (DKK)"].sum()

st.write(f"Total rows: {total_rows}")
st.write(f"Total Markedsværdi (DKK): {total_markedsværdi:,.2f}")

# Layout the plots side by side
col1, col2 = st.columns(2)

with col1:
    st.write("Comparison of Selected Regions (Amount of Rows):")

    if not filtered_df.empty:
        try:
            # Pivot the data to prepare for stacked bar plot (amount of rows)
            type_counts = filtered_df.pivot_table(
                index="Kommune", columns="Type", aggfunc="size", fill_value=0
            )

            if not type_counts.empty:
                fig, ax = plt.subplots(figsize=(10, 6))

                # Plot a stacked bar chart (amount of rows)
                type_counts.plot(kind="bar", stacked=True, ax=ax)

                ax.set_xlabel("Kommune")
                ax.set_ylabel("Number of Entries")
                ax.set_title("Distribution of Types by Kommune (Amount of Rows)")
                ax.legend(title="Type")
                ax.tick_params(axis="x", rotation=45)

                # Display the plot
                st.pyplot(fig)
            else:
                st.write("No data available for plotting.")
        except TypeError as e:
            st.write(f"An error occurred while plotting: {e}")
    else:
        st.write("No data available for the selected Kommune.")

with col2:
    st.write("Comparison of Selected Regions (Total Markedsværdi):")

    if not filtered_df.empty:
        try:
            # Pivot the data to prepare for stacked bar plot (total Markedsværdi)
            type_sums = filtered_df.pivot_table(
                index="Kommune",
                columns="Type",
                values="Markedsværdi (DKK)",
                aggfunc="sum",
                fill_value=0,
            )

            if not type_sums.empty:
                fig, ax = plt.subplots(figsize=(10, 6))

                # Plot a stacked bar chart (total Markedsværdi)
                type_sums.plot(kind="bar", stacked=True, ax=ax)

                ax.set_xlabel("Kommune")
                ax.set_ylabel("Total Markedsværdi (DKK)")
                ax.set_title("Distribution of Total Markedsværdi by Kommune and Type")
                ax.legend(title="Type")
                ax.tick_params(axis="x", rotation=45)

                # Display the plot
                st.pyplot(fig)
            else:
                st.write("No data available for plotting.")
        except TypeError as e:
            st.write(f"An error occurred while plotting: {e}")
    else:
        st.write("No data available for the selected Kommune.")
