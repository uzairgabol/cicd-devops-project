from flask import Flask, request, jsonify, render_template, redirect, url_for
from dotenv import load_dotenv
import os

app = Flask(__name__)

data_store = {}

load_dotenv()

host = os.getenv("APP_HOST", "0.0.0.0")
port = os.getenv("APP_PORT", 5000)


@app.route("/")
def home():
    return render_template("index.html", data=data_store)


@app.route("/item", methods=["POST"])
def create_item():
    item = request.json
    item_id = str(item.get("id"))
    if item_id in data_store:
        return jsonify({"error": "Item already exists"}), 400
    data_store[item_id] = item
    return jsonify({"message": "Item created", "item": item}), 201


@app.route("/item/<item_id>", methods=["GET"])
def get_item(item_id):
    item = data_store.get(item_id)
    if not item:
        return jsonify({"error": "Item not found"}), 404
    return jsonify(item)


@app.route("/item/<item_id>", methods=["PUT"])
def update_item(item_id):
    if item_id not in data_store:
        return jsonify({"error": "Item not found"}), 404
    data_store[item_id] = request.json
    return jsonify({"message": "Item updated", "item": data_store[item_id]})


@app.route("/item/<item_id>", methods=["DELETE"])
def delete_item(item_id):
    if item_id not in data_store:
        return jsonify({"error": "Item not found"}), 404
    del data_store[item_id]
    return jsonify({"message": "Item deleted"})


@app.route("/items", methods=["GET"])
def get_all_items():
    return jsonify(data_store)


@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "ok"}), 200


if __name__ == "__main__":
    app.run(debug=True, host=host, port=port)
