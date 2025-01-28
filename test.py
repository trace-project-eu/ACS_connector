from handle_requests import *
from storage_utils import *

def main():

    # # Load the Excel file
    # file_path1 = 'resources/Shipment-Good_example-2_new.xlsx'
    # file_path2 = 'resources/Vehicle-Load_example.xlsx'
    #
    # json = handle_shipment_request(file_path1)
    # print(json)
    # json = handle_vehicle_request(file_path2)
    # print(json)

    json_test = {
        "weightCapacity": 0,
        "volumeCapacity": 0,
        "dimensions": "string",
        "loadSpecialReq": "string",
        "stable": True,
        "loadType": "Refrigerator",
        "fullyLoaded": True,
        "vehicle": None
    }

    post_load(json_test)



if __name__ == "__main__":
    main()