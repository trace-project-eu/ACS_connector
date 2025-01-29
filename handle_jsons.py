from datetime import datetime
import uuid
import json
import math
from storage_utils import *

# def generate_shipment_json_old(excel_data):
#
#     all_shipments = []
#     for sheet, variables in excel_data.items():
#         sheet_jsons = []
#         for row in variables:
#             shipment_data = row
#
#             shipment_json = {
#                 "ShipmentID": str(uuid.uuid4()),
#                 "Origin": handle_null(shipment_data[1]),
#                 "Destination": handle_null(shipment_data[2]),
#                 "ShipmentWeight": handle_null(shipment_data[3]),
#                 "ShipmentVolume": handle_null(shipment_data[4]),
#                 "ShipmentType": None,
#                 "ShipmentStatus": "Request imported to trace",
#                 "PickUpDate": str(parse_date(handle_null(shipment_data[8]))),
#                 "DeliveryDate": str(parse_date(handle_null(shipment_data[9]))),
#                 "Priority": handle_null(shipment_data[10]),
#                 "RespLogisticsCo": "ACS",
#                 "ScheduledDateDelivery": str(parse_date(handle_null(shipment_data[11]))),
#                 "DeliveryTimeWindow": handle_null(shipment_data[12]),
#                 "ShipmentExternalID": handle_null(shipment_data[13]),
#                 "Good": [
#                     {
#                         "GoodID": str(uuid.uuid4()),
#                         "GoodDescription": None,
#                         "GoodWeight": handle_null(shipment_data[3]),
#                         "GoodVolume": handle_null(shipment_data[4]),
#                         "SpecialRequirements": handle_null(
#                             f'Receiver\'s telephone: {handle_null(shipment_data[14])} | ACS Endpoint: {handle_null(shipment_data[15])} | Volumetric weight: {handle_null(shipment_data[16])}'
#                         ),
#                         "GoodType": None,
#                         "Dimensions": handle_null(f'{shipment_data[5]} x {shipment_data[6]} x {shipment_data[7]}'),
#                         "RespLogisticsCo": "ACS",
#                         "GoodExternalID": handle_null(shipment_data[13])
#                     }
#                 ]
#             }
#
#             print("\n", json.dumps(shipment_json, ensure_ascii=False, indent=4))
#             sheet_jsons.append(shipment_json)
#
#         all_shipments.append(sheet_jsons)
#
#     return all_shipments

def generate_shipment_json(shipment_df, good_df):
    # Process data
    shipment_data = shipment_df.to_dict('records')
    good_data = good_df.to_dict('records')
    shipment_jsons = []

    # Group loads by shipment number
    goods_by_shipment = {}
    for good in good_data:
        shipment_no = handle_null(good.get("Corresponding Shipment"))
        if shipment_no not in goods_by_shipment:
            goods_by_shipment[shipment_no] = []
        goods_by_shipment[shipment_no].append({
            # "GoodID": None,
            "goodDescription": handle_null(good.get('Good Description')),
            "goodWeight": handle_null(good.get('Good Weight')),
            "goodVolume": handle_null(good.get('Good Volume')),
            "specialRequirements": handle_null(good.get('Special Requirements')),
            "goodType": handle_null(good.get('Good Type')),
            "dimensions": ",".join(str(handle_null(good.get(dim))) for dim in ['Length (cm)', 'Width (cm)', 'Height (cm)']),
            "respLogisticCo": handle_null(good.get('Resp Logistics Co')),
            "goodExternalID": str(handle_null(good.get('Good External ID')))
        })

    # Combine data and generate JSON
    for shipment in shipment_data:
        shipment_no = handle_null(shipment.get('A/A'))
        combined_data = {
            # "ShipmentID": None,
            "origin": handle_null(shipment.get('Origin')),
            "destination": handle_null(shipment.get('Destination')),
            "shipmentWeight": handle_null(shipment.get('Shipment Weight (kg)')),
            "shipmentVolume": handle_null(shipment.get('Shipment Volume (cm^3)')),
            "shipmentType": handle_null(shipment.get('Shipment Type')),
            "shipmentStatus": handle_null(shipment.get('Shipment Status')),
            "pickUpDate": str(shipment.get('Pick Up Date')),
            "deliveryDate": str(shipment.get('Delivery Date')),
            "priority": handle_null(shipment.get('Priority')),
            "respLogisticCo": handle_null(shipment.get('Resp Logistic Co')),
            "scheduledDateDelivery": handle_null(shipment.get('Scheduled Date Delivery')),
            "deliveryTimeWindow": handle_null(shipment.get('Delivery Time Window')),
            "shipmentExternalID": str(handle_null(shipment.get('Shipment External ID'))),
            "sent_by": None,
            "received_by": None
        }

        shipment_id = post_shipment(combined_data)
        print("\n", json.dumps(combined_data, ensure_ascii=False, indent=4))

        for good in goods_by_shipment[shipment_no]:
            good["shipmentID"] = shipment_id.strip('"')
            print("\n", json.dumps(good, ensure_ascii=False, indent=4))

            post_good(good)
            print("\n", good)


def generate_vehicles_json(vehicle_df, load_df):
    # Process data
    vehicle_data = vehicle_df.to_dict('records')
    load_data = load_df.to_dict('records')
    vehicle_jsons = []

    # Group loads by vehicle number
    loads_by_vehicle = {}
    for load in load_data:
        vehicle_no = load["Corresponding Vehicle"]
        if vehicle_no not in loads_by_vehicle:
            loads_by_vehicle[vehicle_no] = []
        loads_by_vehicle[vehicle_no].append({
            # "LoadID": None,
            "weightCapacity": handle_null(load.get('Weight Capacity (kg)')),
            "volumeCapacity": handle_null(load.get('Volume Capacity (cm^3)')),
            "dimensions": ",".join(str(handle_null(load.get(dim))) for dim in ['Length (cm)', 'Width (cm)', 'Height (cm)']),
            "loadSpecialReq": handle_null(load.get('Load Special Req')),
            "stable": handle_null(bool(load.get('Stable'))),
            "loadType": handle_null(load.get('Load Type')),
            "fullyLoaded": handle_null(bool(load.get('Fully Loaded')))
        })

    # Combine data and generate JSON
    for vehicle in vehicle_data:
        vehicle_no = vehicle['A/A']
        combined_data = {
            # "VehicleID": None,
            "vehicleType": handle_null(vehicle.get('VehicleType')),
            "vehicleStatus": handle_null(vehicle.get('VehicleStatus')),
            "shareable": handle_null(bool(vehicle.get('Shareable'))),
            "operationalCost": handle_null(vehicle.get('Operational Cost (Euro/hour)')),
            "nominalConsumption": handle_null(vehicle.get('Nominal Consumption [Fuel Type]/hour')),
            "nominalRange": handle_null(vehicle.get('Nominal Range (m)')),
            "nominalSpeed": handle_null(vehicle.get('Nominal Speed (m/s)')),
            "fuelType": handle_null(vehicle.get('Fuel Type')),
            "loadServiceTime": handle_null(vehicle.get('Load Service Time (sec)')),
            "unloadServiceTime": handle_null(vehicle.get('Unload Service Time (sec)')),
            "vehicleExternalID": handle_null(vehicle.get('Vehicle External ID')),
            "belongs_to": None,
            "transportationModes": [

            ]
            # "loads": handle_null(loads_by_vehicle.get(vehicle_no, []))
        }

        vehicle_id = post_vehicle(combined_data)
        print("\n", json.dumps(combined_data, ensure_ascii=False, indent=4))

        for load in loads_by_vehicle[vehicle_no]:
            load["vehicle"] = vehicle_id.strip('"')
            print("\n", json.dumps(load, ensure_ascii=False, indent=4))

            post_load(load)
            print("\n", load)


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