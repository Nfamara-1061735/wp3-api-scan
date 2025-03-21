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

        target_status = request.args.get('status', None)

        if not target_status:
            abort(422)

        # Verify credentials
        if target_role == 'peer':
            if (user and self.verify_role(user, target_role)
                    and verify_password(password, user.password, user.salt)
                    and self.verify_peer_status(user, target_status)):
                session["user"] = {
                'id': user.user_id,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
            }  # Storing authentication using a session
                return {"success": True}
            else:
                if not verify_password(password, user.password, user.salt):
                    return {"success": False, "message": "Verkeerde gebruikersnaam of wachtwoord"}
                if not self.verify_peer_status(user, target_status):
                    return {"success": False, "message": "Uw account is (nog) niet goedgekeurd."}

        elif target_role == 'admin':
            if (user and self.verify_role(user, target_role)
                    and verify_password(password, user.password, user.salt)):
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
    def verify_peer_status(user: Users, target_status: str):
        if not user:
            return

        if target_status == '2':
            return True
        else:
            return False