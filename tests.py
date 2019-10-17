from unittest import TestCase, main as unittest_main, mock
from bson.objectid import ObjectId
from app import app

sample_event_id = ObjectId('5d55cffc4a3d4031f42827a3')
sample_event = {
    'title': 'Storytime',
    'description': 'Storytime with music',
    'age_range': '1-3 yrs old',
    'location': 'San Anselmo Library',
    'date': 'November 15, 2019',
    'category': 'educational'
}
sample_form_data = {
    'title': sample_event['title'],
    'description': sample_event['description'],
    'age_range': sample_event['age_range'],
    'location': sample_event['location'],
    'date': sample_event['date'],
    'category': sample_event['category']    
}

class EventsTest(TestCase):
    """Flask tests"""

    def setUp(self):

        self.client = app.test_client()

        app.config['TESTING'] = True

    def test_home(self):
        """Test the homepage."""
        result = self.client.get('/')
        self.assertEqual(result.status, '200 OK')
        self.assertIn(b'Event', result.data)

    def test_new(self):
        """Test the new event creation page."""
        result = self.client.get('/events/new')
        self.assertEqual(result.status, '200 OK')
        self.assertIn(b'New Event', result.data)
    
    @mock.patch('pymongo.collection.Collection.find_one')
    def test_show_event(self, mock_find):
        """Test showing a single event"""
        mock_find.return_value = sample_event

        result = self.client.get(f'/events/{sample_event_id}')
        self.assertEqual(result.status, '200 OK')
        self.assertIn(b'Storytime', result.data)
    
    @mock.patch('pymongo.collection.Collection.find_one')
    def test_edit_event(self, mock_find):
        """Test editing a single event"""
        mock_find.return_value = sample_event

        result = self.client.get(f'events/{sample_event_id}/edit')
        self.assertEqual(result.status, '200 OK')
        self.assertIn(b'Storytime', result.data)
    
    @mock.patch('pymongo.collection.Collection.insert_one')
    def test_submit_event(self, mock_insert):
        """Test submitting a new event"""
        result = self.client.post('/events', data=sample_form_data)

        # After submitting, should redirect to that event's page
        self.assertEqual(result.status, '302 FOUND')
        mock_insert.asser_called_with(sample_event)

    @mock.patch('pymongo.collection.Collection.update_one')
    def test_update_event(self, mock_update):
        result = self.client.post(f'/events/{sample_event_id}', data=sample_form_data)

        self.assertEqual(result.status, '302 FOUND')
        mock_update.assert_called_with(
            {'_id': sample_event_id},
            {'$set':sample_event})
    
    @mock.patch('pymongo.collection.Collection.delete_one')
    def test_delete_event(self, mock_delete):
        form_data = {'_method': 'DELETE'}
        result = self.client.post(f'/events/{sample_event_id}/delete', data=form_data)

        self.assertEqual(result.status, '302 FOUND')
        mock_delete.assert_called_with(
            {'_id': sample_event_id})



if __name__ == '__main__':
    unittest_main()
