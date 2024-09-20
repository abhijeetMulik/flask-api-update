import pymongo
import logging
from bson import ObjectId
from flask import Flask, request
from pymongo import MongoClient

from base_response import BaseResponse
from user import User
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Set up logger
logging.basicConfig(filename='app.log',
                    level=logging.ERROR,
                    format='%(asctime)s - %(levelname)s - %(message)s')

logger = logging.getLogger(__name__)

# Constants loaded from environment
AUTHORIZATION_TOKEN = os.getenv('AUTHORIZATION_TOKEN')
MONGO_URI = os.getenv('MONGO_URI')
DATABASE_NAME = os.getenv('DATABASE_NAME')
COLLECTION_NAME = os.getenv('COLLECTION_NAME')

# MongoDB Setup
client = MongoClient(MONGO_URI)
db = client[DATABASE_NAME]
user_collection = db[COLLECTION_NAME]

@app.route('/user', methods=['PUT'])
def update_user():
    try:
        # Check authorization
        auth_header = request.headers.get('Authorization')
        if auth_header != AUTHORIZATION_TOKEN:
            return BaseResponse(status="failure", reason="Unauthorized", code=401).to_json()

        # validate session token
        session_token = request.headers.get('session_token')
        if not session_token:
            return BaseResponse(status="failure", reason="Session token missing", code=400).to_json()

        # Parse JSON body:
        body = request.get_json()

        # Mask password and other sensitive information before logging in production.
        logger.info(f"Request Body: {body}")

        if not body:
            return BaseResponse(status="failure", reason="Invalid JSON", code=400).to_json()
        user_id = body.get("user_id")
        if not user_id:
            return BaseResponse(status="failure", reason="Missing user_id", code=400).to_json()
        try:
            user_oid = ObjectId(user_id)
        except Exception as e:
            return BaseResponse(status="failure", reason="Invalid user ID format", code=400).to_json()

        # Check if user exists in database
        user_record = user_collection.find_one({"_id": user_oid, "session_token": session_token})
        logger.info(f"User Record: {user_record}")
        if not user_record:
            return BaseResponse(status="failure", reason="User not found or session token invalid", code=404).to_json()

        # Map database record to User object
        user = User.from_dictionary(user_record)

        # Update user object from request body
        user.update_user(body)

        # Update database record
        result = user_collection.update_one({"_id": user_oid}, {"$set": user.convert_to_dictionary()})

        if result.modified_count == 0:
            return BaseResponse(status="failure", reason="No updates made to the user", code=400).to_json()

        # Successful update
        return BaseResponse(status="success", reason="Record in database updated successfully !", code=200).to_json()

    except pymongo.errors.ConnectionFailure:
        logger.error("Database connection failed", exc_info=True)
        return BaseResponse(status="failure", reason="Database is not available", code=500).to_json()

    except Exception as e:
        # Log the error
        logger.error(f"Internal server error: {str(e)}", exc_info=True)
        return BaseResponse(status="failure", reason="Internal server error", code=500).to_json()

if __name__ == '__main__':
    app.run(debug=True)
