from flask import Blueprint, request, jsonify

from app.extensions import connect_mongo

webhook_bp = Blueprint('webhook_bp', __name__)
db = connect_mongo()

@webhook_bp.route('/webhook/receiver', methods=['POST'])
def webhook_receiver():
    data = request.json

    # Determine action type (push / pull_request / merge)
    action_type = None
    if "pusher" in data:
        action_type = "push"
        author = data["pusher"]["name"]
        to_branch = data["ref"].split("/")[-1]
        from_branch = None
    elif "pull_request" in data and data["action"] == "opened":
        action_type = "pull_request"
        author = data["pull_request"]["user"]["login"]
        from_branch = data["pull_request"]["head"]["ref"]
        to_branch = data["pull_request"]["base"]["ref"]
    elif "pull_request" in data and data["action"] == "closed" and data["pull_request"]["merged"]:
        action_type = "merge"
        author = data["pull_request"]["user"]["login"]
        from_branch = data["pull_request"]["head"]["ref"]
        to_branch = data["pull_request"]["base"]["ref"]
    else:
        return jsonify({"status": "ignored"}), 200

    # Save in MongoDB
    db.events.insert_one({
        "action": action_type,
        "author": author,
        "from_branch": from_branch,
        "to_branch": to_branch,
        "timestamp": data.get("repository", {}).get("pushed_at", None)
    })

    return jsonify({"status": "success"}), 200

print("WEBHOOK RECEIVED")
print(data)
