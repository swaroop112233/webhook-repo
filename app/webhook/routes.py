from flask import Blueprint, json, request, jsonify
from app.extensions import mongo

webhook = Blueprint('webhook', __name__, url_prefix='/webhook')

@webhook.route('/receiver', methods=["POST"])
def receiver():
    data = request.json

    # ✅ Save the data to MongoDB
    mongo.db.events.insert_one(data)

    # ✅ Return success response
    return jsonify({"status": "saved"}), 200
