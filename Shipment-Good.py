import pandas as pd
import json
import os
import handle_jsons

def main():
    # File path
    file_path = 'resources/Shipment-Good_example-2_new.xlsx'

    # Read Excel file
    shipment_df = pd.read_excel(file_path, sheet_name='Shipments')
    good_df = pd.read_excel(file_path, sheet_name='Goods')
    handle_jsons.generate_shipment_json(shipment_df, good_df)

if __name__ == "__main__":
    main()