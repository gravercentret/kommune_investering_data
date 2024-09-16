# Create a new function that applies styling only to the top 1000 rows
def color_rows_limited(row, row_index):
    """
    Apply coloring only if the row index is within the first 1000 rows.
    """
    if row_index < 5000:
        if row["Problematisk ifølge:"] != None:
            return ["background-color: lightcoral"] * len(row)
        else:
            return [""] * len(row)
    else:
        return [""] * len(row)  # No styling for rows beyond 1000

def color_one_column(val):
    color = 'red' if val != None else ''
    return f'background-color: {color}'