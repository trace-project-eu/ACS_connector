import json
import uuid
import math

def generate_shipment_json(excel_data):

    all_shipments = []
    for sheet, variables in excel_data.items():
        sheet_jsons = []
        for row in variables:
            shipment_data = row

            shipment_json = {
                "ShipmentID": str(uuid.uuid4()),
                "Origin": handle_null(shipment_data[1]),
                "Destination": handle_null(shipment_data[2]),
                "Weight": handle_null(shipment_data[3]),
                "Volume": handle_null(shipment_data[4]),
                "Type": None,
                "Status": "Request imported to trace",
                "PickUpDate": handle_null(shipment_data[8]),
                "DeliveryDate": handle_null(shipment_data[9]),
                "Priority": handle_null(shipment_data[10]),
                "RespLogisticsCo": "ACS",
                "ScheduledDelivery": handle_null(shipment_data[11]),
                "DeliveryTimeWindow": handle_null(shipment_data[12]),
                "Good": [
                    {
                        "GoodID": str(uuid.uuid4()),
                        "Description": None,
                        "Weight": handle_null(shipment_data[3]),
                        "Volume": handle_null(shipment_data[4]),
                        "SpecialRequirements": handle_null(
                            f'Voucher: {shipment_data[13]} | Receiver\'s telephone: {shipment_data[14]} | ACS Endpoint: {shipment_data[15]} | Volumetric weight: {shipment_data[16]}'
                        ),
                        "Type": None,
                        "Dimensions": handle_null(f'{shipment_data[5]} x {shipment_data[6]} x {shipment_data[7]}'),
                        "RespLogisticsCo": "ACS"
                    }
                ]
            }

            print("\n", json.dumps(shipment_json, ensure_ascii=False, indent=4))
            sheet_jsons.append(shipment_json)

        all_shipments.append(sheet_jsons)

    return all_shipments

def handle_null(value):
    if value is None or value == "" or (isinstance(value, float) and math.isnan(value)) or str(value).lower() == "nan":
        return None
    return value