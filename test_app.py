import unittest
from unittest.mock import patch
from app import app
from bson import ObjectId
import json

class TestUpdateUser(unittest.TestCase):

    def setUp(self):
        """Setup test environment"""
        self.app = app.test_client()
        self.app.testing = True

    @patch('app.user_collection')
    def test_update_success(self, mock_user_collection):
        """Test successful user update"""
        mock_user_collection.find_one.return_value = {
            "_id": ObjectId("66b3d17ce6d8e2f5b93324d3"),
            "session_token": "rbvkur79jksfu_shjhu"
        }
        mock_user_collection.update_one.return_value.modified_count = 1

        headers = {
            "Authorization": "Bearer laurhln7t4gkhlnfsp7ywho_hlsfl",
            "session_token": "rbvkur79jksfu_shjhu",
            "Content-Type": "application/json"
        }
        body = {
            "user_id": "66b3d17ce6d8e2f5b93324d3",
            "first_name": "Miami",
            "password": "billmd124Pass$",
            "updated_datetime": "2024-08-07T22:26:12.111Z"
        }

        # Send PUT request
        response = self.app.put('/user', headers=headers, data=json.dumps(body))

        # Assert the response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['status'], 'success')

    @patch('app.user_collection')
    def test_update_unauthorized(self, mock_user_collection):
        """Test unauthorized request"""

        headers = {
            "Authorization": "Bearer invalid_token",  # Invalid token
            "session_token": "rbvkur79jksfu_shjhu",
            "Content-Type": "application/json"
        }
        body = {
            "user_id": "66b3d17ce6d8e2f5b93324d3",
            "first_name": "Miami",
            "password": "billmd124Pass$",
            "updated_datetime": "2024-08-07T22:26:12.111Z"
        }

        # Send PUT request
        response = self.app.put('/user', headers=headers, data=json.dumps(body))

        # Assert the response
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json['status'], 'failure')
        self.assertEqual(response.json['reason'], 'Unauthorized')

    @patch('app.user_collection')
    def test_update_user_not_found(self, mock_user_collection):
        """Test user not found scenario"""

        mock_user_collection.find_one.return_value = None

        headers = {
            "Authorization": "Bearer laurhln7t4gkhlnfsp7ywho_hlsfl",
            "session_token": "rbvkur79jksfu_shjhu",
            "Content-Type": "application/json"
        }
        body = {
            "user_id": "66b3d17ce6d8e2f5b93324d3",
            "first_name": "Miami",
            "password": "billmd124Pass$",
            "updated_datetime": "2024-08-07T22:26:12.111Z"
        }

        # Send PUT request
        response = self.app.put('/user', headers=headers, data=json.dumps(body))

        # Assert the response
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json['status'], 'failure')
        self.assertEqual(response.json['reason'], 'User not found or session token invalid')

    @patch('app.user_collection')
    def test_update_invalid_user_id(self, mock_user_collection):
        """Test invalid user ID format"""

        headers = {
            "Authorization": "Bearer laurhln7t4gkhlnfsp7ywho_hlsfl",
            "session_token": "rbvkur79jksfu_shjhu",
            "Content-Type": "application/json"
        }
        body = {
            "user_id": "invalid_user_id",  # Invalid ObjectId format
            "first_name": "Miami",
            "password": "billmd124Pass$",
            "updated_datetime": "2024-08-07T22:26:12.111Z"
        }

        # Send PUT request
        response = self.app.put('/user', headers=headers, data=json.dumps(body))

        # Assert the response
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['status'], 'failure')
        self.assertEqual(response.json['reason'], 'Invalid user ID format')

if __name__ == '__main__':
    unittest.main()
