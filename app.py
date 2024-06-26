from flask import Flask, render_template, request, jsonify
import db
from dateutil import parser
app = Flask(__name__)

collection = db.db_connection()


def parse_event(event):
    if 'pull_request' in event:
        action_type = 'PULL_REQUEST'
        author = event['pull_request']['user']['login']
        from_branch = event['pull_request']['head']['ref']
        to_branch = event['pull_request']['base']['ref']
        timestamp = parser.isoparse(event['pull_request']['created_at'])
        request_id = str(event['pull_request']['id'])
        return request_id, author, action_type, from_branch, to_branch, timestamp
    
    elif 'pusher' in event:
        action_type = 'PUSH'
        author = event['pusher']['name']
        from_branch = None
        to_branch = event['ref'].split('/')[-1]
        timestamp = parser.isoparse(event['head_commit']['timestamp'])
        request_id = event['head_commit']['id']
        return request_id, author, action_type, from_branch, to_branch, timestamp

    elif 'action' in event and event['action'] == 'closed' and event['pull_request']['merged']:
        action_type = 'MERGE'
        author = event['pull_request']['user']['login']
        from_branch = event['pull_request']['head']['ref']
        to_branch = event['pull_request']['base']['ref']
        timestamp = parser.isoparse(event['pull_request']['merged_at'])
        request_id = str(event['pull_request']['id'])
        return request_id, author, action_type, from_branch, to_branch, timestamp

    return None


def create_event_data(request_id, author, action_type, from_branch, to_branch, timestamp):
    return {
        'request_id': request_id,
        'author': author,
        'action': action_type,
        'from_branch': from_branch,
        'to_branch': to_branch,
        'timestamp': timestamp.strftime('%Y-%m-%dT%H:%M:%S')
    }


@app.route("/webhook", methods=['POST'])
def webhook():
    if request.method == "POST":
        event = request.json
        parsed_event = parse_event(event)

        if not parsed_event:
            return jsonify({"msg": "Event not handled"}), 200
        
        request_id, author, action, from_branch, to_branch, timestamps = parsed_event
        
        event_data = create_event_data(request_id, author, action, from_branch, to_branch, timestamps)

        collection.insert_one(event_data)
        
        print(jsonify({"msg": "Event received"}))
        return jsonify({"msg": "Event received"}), 200
    

@app.route("/events", methods=["GET"])
def get_events():
    events = list(collection.find().sort('timestamp', -1).limit(10))
    for event in events:
        event['_id'] = str(event['_id'])
    return jsonify(events)


@app.route("/")
def index():
    return render_template("index.html")


if __name__ == '__main__':
    app.run(port=5000, debug=True)