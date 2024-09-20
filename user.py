from bson import ObjectId
from datetime import datetime

class User:

    def __init__(self, _id: ObjectId, first_name: str, middle_name: str, last_name: str,
                password: str, phone: str, session_token: str,
                created_datetime: datetime, updated_datetime: datetime):
        self._id = _id
        self.first_name = first_name
        self.middle_name = middle_name
        self.last_name = last_name
        self.password = password
        self.phone = phone
        self.session_token = session_token
        self.created_datetime = created_datetime
        self.updated_datetime = updated_datetime

    # Convert MongoDB record to User object
    @classmethod
    def from_dictionary(cls, data: dict):
        return cls(
            _id=data["_id"],
            first_name=data.get("first_name"),
            middle_name=data.get("middle_name"),
            last_name=data.get("last_name"),
            password=data.get("password"),
            phone=data.get("phone"),
            session_token=data.get("session_token"),
            created_datetime=data.get("created_datetime"),
            updated_datetime=data.get("updated_datetime")
        )

    # Convert User object to a dict for MongoDB operations
    def convert_to_dictionary(self):
        return {
            "_id": self._id,
            "first_name": self.first_name,
            "middle_name": self.middle_name,
            "last_name": self.last_name,
            "password": self.password,
            "phone": self.phone,
            "session_token": self.session_token,
            "created_datetime": self.created_datetime,
            "updated_datetime": self.updated_datetime
        }

    # Update fields of the User model from a partial update request
    def update_user(self, data: dict):
        if "first_name" in data:
            self.first_name = data["first_name"]
        if "middle_name" in data:
            self.middle_name = data["middle_name"]
        if "last_name" in data:
            self.last_name = data["last_name"]
        if "password" in data:
            self.password = data["password"]  # Hash the password in production
        if "phone" in data:
            self.phone = data["phone"]
        if "session_token" in data:
            self.session_token = data["session_token"]
        if "updated_datetime" in data:
            self.updated_datetime = datetime.fromisoformat(data["updated_datetime"].replace("Z", "+00:00"))

