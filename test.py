from handle_requests import *

def main():

    # # Load the Excel file
    # file_path = 'resources/Shipment-Good_example-1.xlsx'
    #
    # excel_data = pd.ExcelFile(file_path)
    #
    # data = extract_excel_data(excel_data)
    #
    # jsons = generate_shipment_json_old(data)
    # print()

    # json = handle_vehicle_request()
    json = handle_shipment_request()
    print(json)



if __name__ == "__main__":
    main()