from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId

client = MongoClient()
db = client.Fun_Finder
events = db.events

app = Flask(__name__)

@app.route('/')
def index():
    """Return homepage."""
    return render_template('home.html', msg='Flask is cool!')

#  events = [
#     { 'title': 'Storytime', 'description': 'Free storytime' },
#     { 'title': 'Movie in the park', 'description': 'Cinderella' }
# ]

@app.route('/events')
def events_index():
    """Show all events."""
    return render_template('events_index.html', events=events.find())

@app.route('/events/new')
def new_event():
    """Create a new event."""
    return render_template('new_event.html')

# @app.route('/events', methods=['POST'])
# def event_submit():
#     """Submit a new event."""
#     print(request.form.to_dict())
#     return redirect(url_for('events_index'))

@app.route('/events', methods=['POST'])
def event_submit():
    """Submit a new event."""
    event = {
        'title': request.form.get('title'),
        'description': request.form.get('description'),
        'age_range': request.form.get('age_range'),
        'location': request.form.get('location'),
        'date': request.form.get('date'),
        'category': request.form.get('category')
    }
    event_id = events.insert_one(event).inserted_id
    return redirect(url_for('show_event',event_id=event_id))

@app.route('/events/<event_id>')
def show_event(event_id):
    """Show a single event."""
    event = events.find_one({'_id': ObjectId(event_id)})
    return render_template('show_event.html', event=event)

# @app.route('/events/')
