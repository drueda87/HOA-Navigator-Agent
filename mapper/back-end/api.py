from flask import Flask, jsonify
from db_queries import get_property_data

app = Flask(__name__)

@app.route("/properties", methods=["GET"])
def get_properties():
    """API endpoint to fetch property data."""
    properties = get_property_data()
    return jsonify(properties)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
