import pandas as pd

def extract_excel_data(excel_data):

    # Dictionary to store the sheets and their variables
    sheets_variables = {}

    # Process each sheet
    for sheet_name in excel_data.sheet_names:
        df = excel_data.parse(sheet_name)  # Read the sheet into a DataFrame

        # Convert each cell to a variable, use a list of lists for all cells
        variables_array = df.values.tolist()
        sheets_variables[sheet_name] = variables_array

    # Print the resulting variables for demonstration
    print("Extracted data:")
    for sheet, variables in sheets_variables.items():
        print(f"Sheet: {sheet}")
        for row in variables:
            print(row)

    return sheets_variables