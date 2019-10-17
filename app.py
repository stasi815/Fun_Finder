from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId
import os

host = os.environ.get('MONGODB_URI', 'mongodb://localhost:27017/Fun_Finder')
client = MongoClient(host=f'{host}?retryWrites=false')
db = client.get_default_database()
events = db.events

app = Flask(__name__)

@app.route('/')
def index():
    """Return homepage."""
    return render_template('home.html', msg='Welcome to Fun Finder!')

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
    return render_template('new_event.html', event={}, title='New Event')

@app.route('/events', methods=['POST'])
def event_submit():
    """Submit a new event."""
    event = {
        'title': request.form.get('title'),
        'description': request.form.get('description'),
        'age_range': request.form.get('age_range'),
        'location': request.form.get('location'),
        'date': request.form.get('date'),
        'category': request.form.get('category'),
        'created_at': datetime.now()
    }
    event_id = events.insert_one(event).inserted_id
    return redirect(url_for('show_event',event_id=event_id))

@app.route('/events/<event_id>')
def show_event(event_id):
    """Show a single event."""
    event = events.find_one({'_id': ObjectId(event_id)})
    return render_template('show_event.html', event=event)

@app.route('/events/<event_id>/edit')
def edit_event(event_id):
    """Show the edit form for event"""
    event = events.find_one({'_id': ObjectId(event_id)})
    return render_template('edit_event.html', event=event, title='Edit Event')

@app.route('/events/<event_id>', methods=['POST'])
def update_event(event_id):
    """Submit an edited event"""
    updated_event = {
        'title': request.form.get('title'),
        'description': request.form.get('description'),
        'age_range': request.form.get('age_range'),
        'location': request.form.get('location'),
        'date': request.form.get('date'),
        'category': request.form.get('category')
    }
    events.update_one(
        {'_id': ObjectId(event_id)},
        {'$set': updated_event})
    return redirect(url_for('show_event', event_id=event_id))

@app.route('/events/<event_id>/delete', methods=['POST'])
def delete_event(event_id):
    """Delete an event"""
    events.delete_one({'_id': ObjectId(event_id)})
    return redirect(url_for('events_index'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=os.environ.get('PORT', 5000))
