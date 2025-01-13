import pandas as pd
import json
import os
import handle_jsons

def main():
    # File path
    file_path = 'resources/Vehicle-Load_example.xlsx'

    # Read Excel file
    vehicle_df = pd.read_excel(file_path, sheet_name='Vehicles')
    load_df = pd.read_excel(file_path, sheet_name='Loads')
    handle_jsons.generate_vehicles_json(vehicle_df, load_df)

if __name__ == "__main__":
    main()