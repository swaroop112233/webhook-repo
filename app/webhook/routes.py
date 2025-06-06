from flask import Blueprint, request, jsonify
from app.extensions import mongo

webhook = Blueprint('webhook', __name__, url_prefix='/webhook')

@webhook.route('/receiver', methods=["POST"])
def receiver():
    data = request.get_json()

    if not data:
        return jsonify({"error": "Invalid or empty payload"}), 400

    print("Webhook received:", data)

    # ✅ Save the data to MongoDB
    mongo.db.events.insert_one(data)

    # ✅ Return success response
    return jsonify({"status": "saved"}), 200
