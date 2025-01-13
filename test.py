import pandas as pd

from extract_excel_data import extract_excel_data
from handle_jsons import generate_shipment_json

def main():
    # Load the Excel file
    file_path = 'resources/Shipment-Good_example-1.xlsx'
    excel_data = pd.ExcelFile(file_path)

    data = extract_excel_data(excel_data)

    jsons = generate_shipment_json(data)
    print()

if __name__ == "__main__":
    main()