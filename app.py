from flask import Flask, render_template
from pymongo import MongoClient

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
