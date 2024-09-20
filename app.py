import pymongo
import logging
from bson import ObjectId
from flask import Flask, request, jsonify
from pymongo import MongoClient
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
            return jsonify({"status": "failure", "reason": "Unauthorized"}), 401

        # validate session token
        session_token = request.headers.get('session_token')
        if not session_token:
            return jsonify({"status": "failure", "reason": "Session token missing"}), 400

        # Parse JSON body:
        body = request.get_json()

        # Mask password and other sensitive information before logging in production.
        logger.info(f"Request Body: {body}")

        if not body:
            return jsonify({"Status": "failure", "reason": "Invalid JSON"}), 400
        user_id = body.get("user_id")
        if not user_id:
            return jsonify({"Status": "failure", "reason": "Missing user_id"}), 400
        try:
            user_oid = ObjectId(user_id)
        except Exception as e:
            return jsonify({"Status": "failure", "reason": "Invalid user ID format"}), 400

        # Check if user exists in database
        user_record = user_collection.find_one({"_id": user_oid, "session_token": session_token})
        logger.info(f"User Record: {user_record}")
        if not user_record:
            return jsonify({"Status": "failure", "reason": "User not found or session token invalid"}), 404

        # Map database record to User object
        user = User.from_dictionary(user_record)

        # Update user object from request body
        user.update_user(body)

        # Update database record
        result = user_collection.update_one({"_id": user_oid}, {"$set": user.convert_to_dictionary()})

        if result.modified_count == 0:
            return jsonify({"Status": "failure", "reason": "No updates made to the user"}), 400

        # Successful update
        return jsonify({"Status": "success"}), 200

    except pymongo.errors.ConnectionFailure:
        logger.error("Database connection failed", exc_info=True)
        return jsonify({"Status": "failure", "reason": "Database is not available"}), 500

    except Exception as e:
        # Log the error
        logger.error(f"Internal server error: {str(e)}", exc_info=True)
        return jsonify({"Status": "failure", "reason": "Internal server error"}), 500

if __name__ == '__main__':
    app.run(debug=True)
