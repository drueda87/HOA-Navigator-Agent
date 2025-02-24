from flask import Flask, jsonify
from flask_cors import CORS  # ✅ Import CORS
from db_queries import get_property_data

app = Flask(__name__)
CORS(app)  # ✅ Allow CORS for all domains (for dev only)

@app.route('/properties', methods=['GET'])
def get_properties():
    data = get_property_data()
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
