import streamlit as st
import pandas as pd

# Sample data
data = {
    "Name": ["Alice", "Bob", "Charlie", "David"],
    "Age": [24, 30, 22, 35],
    "Score": [85, 90, 78, 88],
}

# Create a DataFrame
df = pd.DataFrame(data)


# Function to color rows based on condition
def color_rows(row):
    if row["Score"] > 80:
        return ["background-color: lightgreen"] * len(row)
    else:
        return ["background-color: lightcoral"] * len(row)


# Apply the function to the DataFrame
styled_df = df.style.apply(color_rows, axis=1)

# Display the DataFrame in Streamlit
st.dataframe(styled_df)



# # Display basic information
# total_rows = filtered_df.shape[0]
# total_markedsværdi = filtered_df["Markedsværdi (DKK)"].sum()

# st.write(f"Total rows: {total_rows}")
# st.write(f"Total Markedsværdi (DKK): {total_markedsværdi:,.2f}")

# # Layout the plots side by side
# col1, col2 = st.columns(2)

# with col1:
#     st.write("Comparison of Selected Regions (Amount of Rows):")

#     if not filtered_df.empty:
#         try:
#             # Pivot the data to prepare for stacked bar plot (amount of rows)
#             type_counts = filtered_df.pivot_table(
#                 index="Kommune", columns="Type", aggfunc="size", fill_value=0
#             )

#             if not type_counts.empty:
#                 fig, ax = plt.subplots(figsize=(10, 6))

#                 # Plot a stacked bar chart (amount of rows)
#                 type_counts.plot(kind="bar", stacked=True, ax=ax)

#                 ax.set_xlabel("Kommune")
#                 ax.set_ylabel("Number of Entries")
#                 ax.set_title("Distribution of Types by Kommune (Amount of Rows)")
#                 ax.legend(title="Type")
#                 ax.tick_params(axis="x", rotation=45)

#                 # Display the plot
#                 st.pyplot(fig)
#             else:
#                 st.write("No data available for plotting.")
#         except TypeError as e:
#             st.write(f"An error occurred while plotting: {e}")
#     else:
#         st.write("No data available for the selected Kommune.")

# with col2:
#     st.write("Comparison of Selected Regions (Total Markedsværdi):")

#     if not filtered_df.empty:
#         try:
#             # Pivot the data to prepare for stacked bar plot (total Markedsværdi)
#             type_sums = filtered_df.pivot_table(
#                 index="Kommune",
#                 columns="Type",
#                 values="Markedsværdi (DKK)",
#                 aggfunc="sum",
#                 fill_value=0,
#             )

#             if not type_sums.empty:
#                 fig, ax = plt.subplots(figsize=(10, 6))

#                 # Plot a stacked bar chart (total Markedsværdi)
#                 type_sums.plot(kind="bar", stacked=True, ax=ax)

#                 ax.set_xlabel("Kommune")
#                 ax.set_ylabel("Total Markedsværdi (DKK)")
#                 ax.set_title("Distribution of Total Markedsværdi by Kommune and Type")
#                 ax.legend(title="Type")
#                 ax.tick_params(axis="x", rotation=45)

#                 # Display the plot
#                 st.pyplot(fig)
#             else:
#                 st.write("No data available for plotting.")
#         except TypeError as e:
#             st.write(f"An error occurred while plotting: {e}")
#     else:
#         st.write("No data available for the selected Kommune.")
