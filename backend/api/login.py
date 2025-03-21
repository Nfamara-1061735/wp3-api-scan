from flask import request, session
from flask_restful import Resource, reqparse, abort

from backend.database.models import Users
from backend.database.models import PeerExperts
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
        if target_role == 'peer':
            # Check role and password once
            if user and self.verify_role(user, target_role):
                if verify_password(password, user.password, user.salt):
                    print()
                    if self.verify_peer_status(user):
                        session["user"] = {
                            'id': user.user_id,
                            'email': user.email,
                            'first_name': user.first_name,
                            'last_name': user.last_name,
                        }  # Storing authentication using a session
                        return {"success": True}
                    else:
                        return {"success": False, "message": "Uw account is (nog) niet goedgekeurd."}
                else:
                    return {"success": False, "message": "Verkeerde gebruikersnaam of wachtwoord"}
            else:
                return {"success": False, "message": "Verkeerde gebruikersnaam of wachtwoord"}

        elif target_role == 'admin':
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

    @staticmethod
    def verify_peer_status(user: Users):
        if not user or not user.peer_expert_info:
            return False
        if user.peer_expert_info.peer_expert_status_id == 2:
            return True
        else:
            return False