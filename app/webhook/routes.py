from flask import Blueprint, request, jsonify, render_template
from app.extensions import connect_mongo
import datetime  # used to format timestamps

# Create a Flask Blueprint for webhook handling
webhook_bp = Blueprint('webhook_bp', __name__)
db = connect_mongo()

@webhook_bp.route('/webhook/receiver', methods=['POST'])
def webhook_receiver():
    data = request.json

    # Determine the type of GitHub action (push, pull_request, or merge)
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

    # Extract timestamp from the payload (raw Unix timestamp)
    raw_timestamp = data.get("repository", {}).get("pushed_at", None)
    formatted_time = None
    if raw_timestamp:
        formatted_time = datetime.datetime.utcfromtimestamp(raw_timestamp).strftime('%d %B %Y - %I:%M %p UTC')

    # Save formatted data into MongoDB
    db.events.insert_one({
        "action": action_type,
        "author": author,
        "from_branch": from_branch,
        "to_branch": to_branch,
        "timestamp": formatted_time
    })

    return jsonify({"status": "success"}), 200

@webhook_bp.route('/')
def home():
    # Get the latest 10 events, sorted by most recent
    events = list(db.events.find().sort("_id", -1).limit(10))
    return render_template('index.html', events=events)
