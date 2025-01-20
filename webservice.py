from flask import Flask
from handle_requests import *
import json
app = Flask (__name__)
@app.route('/ACS-connector')
def welcome():
    return 'Welcome to the ACS Transformer/Connector Webservice!'

@app.route('/vehicles', methods=['GET'])
def handle_vehicles():
    return handle_vehicle_request()

@app.route('/shipments', methods=['GET'])
def handle_shipments():
    return handle_shipment_request()



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)