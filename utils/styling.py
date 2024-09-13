def color_rows(row):
    """
    Color the row red if the 'Problematisk ifølge:' column is not empty, otherwise leave it unchanged.
    """
    if row["Problematisk ifølge:"] != "":
        return ["background-color: lightcoral"] * len(row)
    else:
        return [""] * len(row)  # No color change if the column is empty