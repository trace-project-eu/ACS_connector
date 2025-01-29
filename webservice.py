from flask import Flask, request, jsonify
from handle_requests import handle_vehicle_request, handle_shipment_request
import os


def create_app():
    app = Flask(__name__)

    @app.route("/ACS-connector")
    def welcome():
        return "Welcome to the ACS Transformer/Connector Webservice!"

    @app.route("/vehicles", methods=["POST"])
    def handle_vehicles():
        # Check if the request contains a file
        if "file" not in request.files:
            print("\n Error: No file part in the request")
            return jsonify({"error": "No file part in the request"}), 400

        file = request.files["file"]

        # Check if the file has a valid name
        if file.filename == "":
            print("\n Error: No selected file")
            return jsonify({"error": "No selected file"}), 400

        # Save the file temporarily
        file_path = os.path.join("/tmp", file.filename)
        file.save(file_path)

        # Process the file and handle the vehicle request
        try:
            result = handle_vehicle_request(file_path)
            os.remove(file_path)  # Clean up the temporary file
            return result
        except Exception as e:
            os.remove(file_path)  # Clean up the temporary file in case of an error
            print("\n Error: ", str(e))
            return jsonify({"error": str(e)}), 500

    @app.route("/shipments", methods=["POST"])
    def handle_shipments():
        # Check if the request contains a file
        if "file" not in request.files:
            print("\n Error: No file part in the request")
            return jsonify({"error": "No file part in the request"}), 400

        file = request.files["file"]

        # Check if the file has a valid name
        if file.filename == "":
            print("\n Error: No selected file")
            return jsonify({"error": "No selected file"}), 400

        # Save the file temporarily
        file_path = os.path.join("/tmp", file.filename)
        file.save(file_path)

        # Process the file and handle the shipment request
        try:
            result = handle_shipment_request(file_path)
            os.remove(file_path)  # Clean up the temporary file
            return result
        except Exception as e:
            os.remove(file_path)  # Clean up the temporary file in case of an error
            print("\n Error: ", str(e))
            return jsonify({"error": str(e)}), 500

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=8080)
