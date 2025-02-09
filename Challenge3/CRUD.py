"""
CRUD module.

This module provides a Flask application to perform CRUD operations on items stored in a JSON file.

Endpoints:
- GET /api/items: Retrieves all items.
- GET /api/items/<id>: Retrieves a specific item by ID.
- POST /api/items: Creates a new item.
- PUT /api/items/<id>: Updates an existing item by ID.
- DELETE /api/items/<id>: Deletes an existing item by ID.
"""

import os
import json
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)
file_path = os.path.join(os.path.dirname(__file__), 'input.json')

# Ensure the JSON file exists
if not os.path.exists(file_path):
    with open(file_path, 'w') as file:
        json.dump([], file)

def read_items(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def write_items(file_path, items):
    with open(file_path, 'w') as file:
        json.dump(items, file, indent=4)

def is_valid_item(item, items):
    """
    Validates the item data.

    Args:
        item (dict): The item data to validate.
        items (list): The list of existing items.

    Returns:
        bool: True if the item is valid, False otherwise.
    """
    if 'id' in item and any(existing_item['id'] == item['id'] for existing_item in items):
        return False
    if 'price' in item and not isinstance(item['price'], (int, float)):
        return False
    return True

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/items', methods=['GET'])
def get_items():
    items = read_items(file_path)
    return jsonify(items)

@app.route('/api/items/<id>', methods=['GET'])
def get_item(id):
    try:
        id = int(id)
    except ValueError:
        return jsonify({"error": "Invalid ID: ID must be an integer"}), 400
    items = read_items(file_path)
    item = next((item for item in items if item['id'] == id), None)
    return jsonify(item) if item else ('', 404)

@app.route('/api/items/search', methods=['GET'])
def search_items():
    query = request.args.get('q', '')
    items = read_items(file_path)
    results = [item for item in items if query.lower() in str(item['id']).lower() or query.lower() in item.get('name', '').lower() or query.lower() in item.get('description', '').lower()]
    return jsonify(results)

@app.route('/api/items', methods=['POST'])
def create_item():
    items = read_items(file_path)
    new_item = request.json
    if not is_valid_item(new_item, items):
        return jsonify({"error": "Invalid item data: ID must be unique and price must be an integer or float"}), 400
    items.append(new_item)
    write_items(file_path, items)
    return jsonify(new_item), 201

@app.route('/api/items/<id>', methods=['PUT'])
def update_item(id):
    items = read_items(file_path)
    item = next((item for item in items if item['id'] == id), None)
    if item:
        updated_data = request.json
        if not is_valid_item(updated_data, items):
            return jsonify({"error": "Invalid item data: price must be an integer or float"}), 400
        item.update(updated_data)
        write_items(file_path, items)
        return jsonify(item)
    return ('', 404)

@app.route('/api/items/<id>', methods=['DELETE'])
def delete_item(id):
    items = read_items(file_path)
    item = next((item for item in items if item['id'] == id), None)
    if item:
        items.remove(item)
        write_items(file_path, items)
        return ('', 204)
    return ('', 404)

@app.errorhandler(Exception)
def handle_exception(e):
    response = {
        "error": str(e)
    }
    return jsonify(response), 500

if __name__ == '__main__':
    app.run(debug=True)
