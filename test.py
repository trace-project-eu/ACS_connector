from handle_requests import *
from storage_utils import *

def main():

    # # Load the Excel file
    # file_path1 = 'resources/Shipment-Good_data.xlsx'
    # file_path2 = 'resources/Vehicle-Load_data.xlsx'
    #
    # json = handle_shipment_request(file_path1)
    # print(json)
    # json = handle_vehicle_request(file_path2)
    # print(json)

    json_test = {
        "origin": "Τεμπών 6, Περιστέρι, 12137",
        "destination": "Πανεπιστημιούπολη Ζωγράφου, Ζωγράφος, 15772, τμήμα πληροφορικής",
        "shipmentWeight": 0.6,
        "shipmentVolume": 250.0,
        "shipmentType": "Standard",
        "shipmentStatus": "Ongoing",
        "pickUpDate": "2024-10-11 00:00:00",
        "deliveryDate": "2024-11-11 00:00:00",
        "priority": 5,
        "respLogisticCo": "ACS",
        "scheduledDateDelivery": None,
        "deliveryTimeWindow": None,
        "shipmentExternalID": "9369529396",
        "sent_by": None,
        "received_by": None
    }

    post_shipment(json_test)



if __name__ == "__main__":
    main()