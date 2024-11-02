from flask import Flask, render_template, request, jsonify
import requests

# Update these URLs to the correct ones for your functions
FAASD_API_URL_persegi = "http://34.236.149.51:8080/function"
FAASD_API_URL_kubus = "http://184.72.133.223:8080/function"

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/luas-persegi', methods=['POST'])
def luas_persegi():
    side_length = request.form.get("side_length")
    print(f"Received side_length: {side_length}")  # Check what value is received

    if side_length is None:
        return jsonify({"error": "side_length parameter is missing"}), 400

    try:
        # Convert to float and process as needed
        side_length = float(side_length)

        # Call the FAASD API
        response = requests.post(f"{FAASD_API_URL_persegi}/luas-persegi", json={"side_length": side_length})
        response.raise_for_status()  # Raise an error for bad responses
        response_data = response.json()

        # Return the area if available
        if 'area' in response_data:
            return jsonify({"area": response_data['area']})
        else:
            return jsonify({"error": "Unable to calculate area"}), 400
    except ValueError:
        return jsonify({"error": "Invalid side_length value"}), 400
    except requests.RequestException as e:
        return jsonify({"error": str(e)}), 500

@app.route('/luas-permukaan-kubus', methods=['POST'])
def luas_permukaan_kubus():
    edge = request.form.get("edge")
    print(f"Received edge: {edge}")  # Check what value is received

    if edge is None:
        return jsonify({"error": "edge parameter is missing"}), 400

    try:
        # Convert to float and process as needed
        edge = float(edge)

        # Call the FAASD API
        response = requests.post(f"{FAASD_API_URL_kubus}/luas-permukaan-kubus", json={"edge": edge})
        response.raise_for_status()  # Raise an error for bad responses
        response_data = response.json()

        # Return the cube surface area if available
        if 'cube_surface_area' in response_data:
            return jsonify({"cube_surface_area": response_data['cube_surface_area']})
        else:
            return jsonify({"error": "Unable to calculate cube surface area"}), 400
    except ValueError:
        return jsonify({"error": "Invalid edge value"}), 400
    except requests.RequestException as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
