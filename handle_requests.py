from logging import warning
import json

import pandas as pd

import handle_jsons


def handle_vehicle_request(file_path):

    # Read Excel file
    vehicle_df = pd.read_excel(file_path, sheet_name='Vehicles')
    load_df = pd.read_excel(file_path, sheet_name='Loads')

    return handle_jsons.generate_vehicles_json(vehicle_df, load_df)

def handle_shipment_request(file_path):

    # Read Excel file
    shipment_df = pd.read_excel(file_path, sheet_name='Shipments')
    good_df = pd.read_excel(file_path, sheet_name='Goods')
    return handle_jsons.generate_shipment_json(shipment_df, good_df)
