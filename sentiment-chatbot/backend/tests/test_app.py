import unittest
import json
import sys
import os

# Add the parent directory to the path to allow imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.main import app

class ChatbotTestCase(unittest.TestCase):
    """This class represents the chatbot test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = app.test_client()
        self.app.testing = True

    def test_chat_endpoint_with_positive_message(self):
        """Test chat endpoint with a positive message."""
        response = self.app.post(
            '/chat',
            data=json.dumps({'message': 'I am happy'}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('bot_response', data)
        self.assertIn('statement_sentiment', data)
        self.assertGreater(data['statement_sentiment']['compound'], 0)

    def test_chat_endpoint_with_negative_message(self):
        """Test chat endpoint with a negative message."""
        response = self.app.post(
            '/chat',
            data=json.dumps({'message': 'I am sad'}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('bot_response', data)
        self.assertIn('statement_sentiment', data)
        self.assertLess(data['statement_sentiment']['compound'], 0)

    def test_chat_endpoint_with_no_message(self):
        """Test chat endpoint with no message."""
        response = self.app.post(
            '/chat',
            data=json.dumps({}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)

if __name__ == "__main__":
    unittest.main()