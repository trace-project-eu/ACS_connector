import requests

def post_vehicle(json_message):

    url = "http://142.132.165.122:9014/api/v1/vehicles"

    response = requests.post(url, json=json_message)
    print(f'\nVehicle written to the database with ID: ', response.text)

    return response.text


def post_load(json_message):
    url = "http://142.132.165.122:9014/api/v1/loads"

    response = requests.post(url, json=json_message)
    print(f'\nLoad written to the database with ID: ', response.text)

    return response.text


def post_shipment(json_message):
    url = "http://142.132.165.122:9014/api/v1/shipments"

    response = requests.post(url, json=json_message)
    print(f'\nShipment written to the database with ID: ', response.text)

    return response.text


def post_good(json_message):
    url = "http://142.132.165.122:9014/api/v1/goods"

    response = requests.post(url, json=json_message)
    print(f'\nGood written to the database with ID: ', response.text)

    return response.text