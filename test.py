from handle_requests import *

def main():

    # Load the Excel file
    file_path1 = 'resources/Shipment-Good_example-2_new.xlsx'
    file_path2 = 'resources/Vehicle-Load_example.xlsx'

    json = handle_shipment_request(file_path1)
    print(json)
    json = handle_vehicle_request(file_path2)
    print(json)



if __name__ == "__main__":
    main()