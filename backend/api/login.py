from flask import request, session
from flask_restful import Resource, reqparse, abort

from backend.database.models import Users
from backend.utils.password import verify_password


class Login(Resource):
    def post(self):
        email: str = request.headers.get('email')
        password: str = request.headers.get('password')

        target_role = request.args.get('role', None)

        if not target_role:
            abort(422)

        user: Users = Users.query.filter_by(email=email).first()

        # Verify credentials
        if user and self.verify_role(user, target_role) and verify_password(password, user.password, user.salt):
            session["user"] = {
                'id': user.user_id,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
            }  # Storing authentication using a session
            return {"success": True}
        else:
            return {"success": False, "message": "Verkeerde gebruikersnaam of wachtwoord"}

    @staticmethod
    def verify_role(user: Users, target_role: str):
        if not user:
            return

        if target_role == 'admin':
            if user.admin_info:
                return True
        elif target_role == 'peer':
            if user.peer_expert_info:
                return True
        return False
