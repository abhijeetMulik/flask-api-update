from flask import jsonify

class BaseResponse:
    def __init__(self, status: str, reason: str, code: int):
        self.status = status
        self.reason = reason
        self.code = code

    def to_json(self):
        """Converts the response to a JSON response with the given HTTP code."""
        response_body = {
            "status": self.status,
            "reason": self.reason
        }
        return jsonify(response_body), self.code
