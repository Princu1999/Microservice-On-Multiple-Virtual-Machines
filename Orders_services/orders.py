from flask import Flask, jsonify, request
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

orders = []

@app.route('/orders', methods=['POST'])
def create_order():
    order_data = request.json
    product_id = order_data.get('product_id')
    user_id = order_data.get('user_id')

    # Verify product exists
    product_response = requests.get(f'http://192.168.56.4:5000/products/{product_id}')
    if product_response.status_code != 200:
        return jsonify({"error": "Product not found"}), 404

    # Verify user exists
    user_response = requests.get(f'http://192.168.56.6:5000/users/{user_id}')
    if user_response.status_code != 200:
        return jsonify({"error": "User not found"}), 404

    new_order = {
        "id": len(orders) + 1,
        "product_id": product_id,
        "user_id": user_id
    }
    orders.append(new_order)
    return jsonify(new_order), 201

@app.route('/orders', methods=['GET'])
def get_orders():
    return jsonify(orders)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
