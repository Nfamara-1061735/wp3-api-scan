from flask import jsonify


def method_not_allowed():
    response = jsonify({"error": "Methode niet toegestaan"})
    response.status_code = 405
    return response
