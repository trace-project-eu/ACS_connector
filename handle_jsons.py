from datetime import datetime
import uuid
import json
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
                "ShipmentWeight": handle_null(shipment_data[3]),
                "ShipmentVolume": handle_null(shipment_data[4]),
                "ShipmentType": None,
                "ShipmentStatus": "Request imported to trace",
                "PickUpDate": str(parse_date(handle_null(shipment_data[8]))),
                "DeliveryDate": str(parse_date(handle_null(shipment_data[9]))),
                "Priority": handle_null(shipment_data[10]),
                "RespLogisticsCo": "ACS",
                "ScheduledDateDelivery": str(parse_date(handle_null(shipment_data[11]))),
                "DeliveryTimeWindow": handle_null(shipment_data[12]),
                "ShipmentExternalID": handle_null(shipment_data[13]),
                "Good": [
                    {
                        "GoodID": str(uuid.uuid4()),
                        "GoodDescription": None,
                        "GoodWeight": handle_null(shipment_data[3]),
                        "GoodVolume": handle_null(shipment_data[4]),
                        "SpecialRequirements": handle_null(
                            f'Receiver\'s telephone: {handle_null(shipment_data[14])} | ACS Endpoint: {handle_null(shipment_data[15])} | Volumetric weight: {handle_null(shipment_data[16])}'
                        ),
                        "GoodType": None,
                        "Dimensions": handle_null(f'{shipment_data[5]} x {shipment_data[6]} x {shipment_data[7]}'),
                        "RespLogisticsCo": "ACS",
                        "GoodExternalID": handle_null(shipment_data[13])
                    }
                ]
            }

            print("\n", json.dumps(shipment_json, ensure_ascii=False, indent=4))
            sheet_jsons.append(shipment_json)

        all_shipments.append(sheet_jsons)

    return all_shipments

def handle_null(value):
    """Returns None for empty, falsy, or NaN values. Otherwise, returns the value."""
    if value is None or value == "" or (isinstance(value, float) and math.isnan(value)) or str(value).lower() == "nan":
        return None
    return value

def parse_date(date_string):
    """Converts a string in 'dd/mm/yyyy' format to a datetime object."""
    try:
        # Correctly use datetime.strptime to parse the date
        return datetime.strptime(date_string, "%d/%m/%Y") if date_string else None
    except ValueError:
        return None  # Return None if the date string is not in the expected format