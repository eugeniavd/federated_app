import sqlite3
from flask import Flask, render_template, request, url_for, flash, redirect
from werkzeug.exceptions import abort
import json
import requests
from datetime import datetime


app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn@app.route('/')

def index():
    conn = get_db_connection()
    events = conn.execute('SELECT * FROM events').fetchall()
    conn.close()
    return render_template('index.html', events=events )

# To create an ActivityPub-compatible Event
def create_activitypub_event(attributed_to, name, content, start_time, location):
    event = {
        "@context": "https://www.w3.org/ns/activitystreams",
        "type": "Event",
        "attributedTo": attributed_to,
        "name": name,
        "content": content,
        "startTime": start_time,
        "location": location,
        "published": datetime.utcnow().isoformat()
    }
    return event

# To send an ActivityPub event to another participant
def send_activitypub_event(event_data, receiver_url):
    headers = {'Content-Type': 'application/json'}
    try:
        response = requests.post(receiver_url, data=json.dumps(event_data), headers=headers)
        if response.status_code == 200:
            return True
        else:
            return False
    except requests.RequestException as e:
        print(f"Error sending event: {e}")
        return False

@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        attributed_to_value = 'https://example.com/user1'
        name_value = 'Event Name'
        content_value = 'Event Content'
        start_time_value = '2023-12-25T12:00:00Z'  
        location_value = 'Event Location'
        updated_value = '2023-12-26T09:00:00Z'  

        # Insert into the local database
        conn = sqlite3.connect('database.db')
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO events (attributedTo, name, content, startTime, location, published, updated)
            VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP, ?)
        """, (attributed_to_value, name_value, content_value, start_time_value, location_value, updated_value))
        conn.commit()
        conn.close()

        # Create an ActivityPub event
        event_data = create_activitypub_event(attributed_to_value, name_value, content_value, start_time_value, location_value)
        
        # Send the ActivityPub event to other participants
        receiver_url = 'https://example.com/receiver-endpoint'  # which is our endpoint????
        send_success = send_activitypub_event(event_data, receiver_url)

        if send_success:
            flash('Event created and sent successfully!', 'success')
        else:
            flash('Failed to send the event.', 'error')
        
        return redirect(url_for('index'))

    return render_template('create.html')

@app.route('/receive-event', methods=['POST'])
def receive_event():
    if request.method == 'POST':
        
        event_data = request.get_json()

        # Save the received event data to the local database
        conn = sqlite3.connect('database.db')
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO events (attributedTo, name, content, startTime, location, published, updated)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            event_data.get('attributedTo'),
            event_data.get('name'),
            event_data.get('content'),
            event_data.get('startTime'),
            event_data.get('location'),
            event_data.get('published'),
            event_data.get('updated')
        ))
        conn.commit()
        conn.close()

        return '', 200  # Respond with success status
    else:
        abort(405)  # Method Not Allowed for non-POST requests


