from flask import Flask, request, render_template
from pymongo import MongoClient
from datetime import datetime

app = Flask(__name__)

# MongoDB connection
client = MongoClient("mongodb+srv://webuser:web1234@cluster0.sv0nyyl.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client["webhookDB"]
collection = db["events"]

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    print("Webhook received:", data)

    action = data.get('action', 'push')
    author = data.get('sender', {}).get('login', 'unknown')
    from_branch = data.get('pull_request', {}).get('head', {}).get('ref', '')
    to_branch = data.get('pull_request', {}).get('base', {}).get('ref', '')
    timestamp = datetime.utcnow().strftime("%d %B %Y - %I:%M %p UTC")

    event = {
        "action": action,
        "author": author,
        "from_branch": from_branch,
        "to_branch": to_branch,
        "timestamp": timestamp
    }

    collection.insert_one(event)
    return "Event received", 200

@app.route('/test')
def test_insert():
    test_event = {
        "action": "push",
        "author": "Jyothi",
        "from_branch": "",
        "to_branch": "main",
        "timestamp": datetime.utcnow().strftime("%d %B %Y - %I:%M %p UTC")
    }
    collection.insert_one(test_event)
    return "Test event inserted!"


@app.route('/')
def index():
    events = list(collection.find().sort('_id', -1))
    return render_template('index.html', events=events)

if __name__ == '__main__':
    app.run(port=5000)
