from datetime import datetime
import uuid
import json
import math

def generate_shipment_json_old(excel_data):

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
            "GoodID": None,
            "GoodDescription": handle_null(good.get('Good Description')),
            "GoodWeight": handle_null(good.get('Good Weight')),
            "GoodVolume": handle_null(good.get('Good Volume')),
            "SpecialRequirements": handle_null(good.get('Special Requirements')),
            "GoodType": handle_null(good.get('Good Type')),
            "Dimensions": [handle_null(good.get('Length (cm)')), handle_null(good.get('Width (cm)')), handle_null(good.get('Height (cm)'))],
            "RespLogisticCo": handle_null(good.get('Resp Logistic Co')),
            "GoodExternalID": handle_null(good.get('Good External ID'))
        })

    # Combine data and generate JSON
    for shipment in shipment_data:
        shipment_no = handle_null(shipment.get('A/A'))
        combined_data = {
            "ShipmentID": None,
            "Origin": handle_null(shipment.get('Origin')),
            "Destination": handle_null(shipment.get('Destination')),
            "ShipmentWeight": handle_null(shipment.get('Shipment Weight (kg)')),
            "ShipmentVolume": handle_null(shipment.get('Shipment Volume (cm^3)')),
            "ShipmentType": handle_null(shipment.get('Shipment Type')),
            "ShipmentStatus": handle_null(shipment.get('Shipment Status')),
            "PickUpDate": str(shipment.get('Pick Up Date')),
            "DeliveryDate": str(shipment.get('Delivery Date')),
            "Priority": handle_null(shipment.get('Priority')),
            "RespLogisticCo": handle_null(shipment.get('Resp Logistic Co')),
            "ScheduledDateDelivery": handle_null(shipment.get('Scheduled Date Delivery')),
            "DeliveryTimeWindow": handle_null(shipment.get('Delivery Time Window')),
            "ShipmentExternalID": handle_null(shipment.get('Shipment External ID')),
            "Goods": handle_null(goods_by_shipment.get(shipment_no, []))
        }

        # shipment_json = json.dumps(combined_data, ensure_ascii=False)
        print("\n", json.dumps(combined_data, ensure_ascii=False, indent=4))
        shipment_jsons.append(combined_data)

    return shipment_jsons

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
            "LoadID": None,
            "WeightCapacity": handle_null(load.get('Weight Capacity (kg)')),
            "VolumeCapacity": handle_null(load.get('Volume Capacity (cm^3)')),
            "Dimensions": [handle_null(load.get('Length (cm)')), handle_null(load.get('Width (cm)')), handle_null(load.get('Height (cm)'))],
            "LoadSpecialReq": handle_null(load.get('Load Special Req')),
            "Stable": handle_null(bool(load.get('Stable'))),
            "LoadType": handle_null(load.get('Load Type')),
            "FullyLoaded": handle_null(bool(load.get('Fully Loaded')))
        })

    # Combine data and generate JSON
    for vehicle in vehicle_data:
        vehicle_no = vehicle['A/A']
        combined_data = {
            "VehicleID": None,
            "VehicleType": handle_null(vehicle.get('VehicleType')),
            "VehicleStatus": handle_null(vehicle.get('VehicleStatus')),
            "Shareable": handle_null(bool(vehicle.get('Shareable'))),
            "OperationalCost": handle_null(vehicle.get('Operational Cost (Euro/hour)')),
            "NominalConsumption": handle_null(vehicle.get('Nominal Consumption [Fuel Type]/hour')),
            "NominalRange": handle_null(vehicle.get('Nominal Range (m)')),
            "NominalSpeed": handle_null(vehicle.get('Nominal Speed (m/s)')),
            "FuelType": handle_null(vehicle.get('Fuel Type')),
            "LoadServiceTime": handle_null(vehicle.get('Load Service Time (sec)')),
            "UnloadServiceTime": handle_null(vehicle.get('Unload Service Time (sec)')),
            "VehicleExternalID": handle_null(vehicle.get('Vehicle External ID')),
            "Loads": handle_null(loads_by_vehicle.get(vehicle_no, []))
        }

        vehicle_json = json.dumps(combined_data, ensure_ascii=False)
        print("\n", json.dumps(combined_data, ensure_ascii=False, indent=4))
        vehicle_jsons.append(combined_data)

        # # Write to JSON file
        # output_file = os.path.join(output_dir, f'vehicle_{vehicle_no}.json')
        # with open(output_file, 'w') as json_file:
        #     json.dump(combined_data, json_file, indent=4)

    return vehicle_jsons

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