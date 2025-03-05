from flask import request, session
from flask_restful import Resource, reqparse

from backend.database.models import Users
from backend.utils.password import verify_password


class Login(Resource):
    def post(self):
        email: str = request.headers.get('email')
        password: str = request.headers.get('password')

        user: Users = Users.query.filter_by(email=email).first()

        # Verify credentials
        if user and verify_password(password, user.password, user.salt):
            session["user"] = email  # Storing authentication using the session
            return {"success": True}
        else:
            return {"success": False, "message": "Incorrect email or password"}
