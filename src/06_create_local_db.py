import pandas as pd
from sqlalchemy import create_engine

data_path = "full_data.xlsx"
df = pd.read_excel(data_path)

# Create an SQLite engine
engine = create_engine("sqlite:///investerings_database.db")

# Save the DataFrame 'df' to the SQLite database
# 'data_table' is the name of the table that will be created in the database
df.to_sql("kommunale_regioner_investeringer", engine, if_exists="replace", index=False)

print("DataFrame has been saved to SQLite database as 'data_table'.")

# Example of a query to retrieve data from the local SQLite database
# Connect to the SQLite database
with engine.connect() as conn:
    # Sample query to select all rows
    query = "SELECT * FROM kommunale_regioner_investeringer WHERE `Kommune` = 'Bornholm';"  # Example query

    # Execute the query and load the result into a new DataFrame
    result_df = pd.read_sql(query, conn)

print(result_df)
