import streamlit as st
import pandas as pd

# Sample data
data = {
    'Name': ['Alice', 'Bob', 'Charlie', 'David'],
    'Age': [24, 30, 22, 35],
    'Score': [85, 90, 78, 88]
}

# Create a DataFrame
df = pd.DataFrame(data)

# Function to color rows based on condition
def color_rows(row):
    if row['Score'] > 80:
        return ['background-color: lightgreen'] * len(row)
    else:
        return ['background-color: lightcoral'] * len(row)

# Apply the function to the DataFrame
styled_df = df.style.apply(color_rows, axis=1)

# Display the DataFrame in Streamlit
st.dataframe(styled_df)
