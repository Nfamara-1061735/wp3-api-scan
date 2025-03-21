from flask import jsonify, session
from flask_restful import abort

from backend import db
from backend.database.models.api_keys_model import ApiKeys
from backend.utils.check_permissions import check_permission_rest
from functools import wraps
from flask import request, abort, g

def method_not_allowed():
    response = jsonify({"error": "Methode niet toegestaan"})
    response.status_code = 405
    return response


# api-key validatie with optional role check
def require_api_key(role: str | None = None):
   def decorator(f):
      @wraps(f)
      def decorated_function(*args, **kwargs):
         if 'user' in session and role:
            if role == 'all':
               target_role = None
            else:
               target_role = role

            # If the user is in the session, delegate to the check_permission_rest decorator
            permission_decorator = check_permission_rest(target_role)  # Create the decorator with the provided role
            return permission_decorator(f)(*args, **kwargs)  # Call the decorated function with the permission check

         api_key_header = request.headers.get("Authorization")

         if not api_key_header or not api_key_header.startswith("Bearer "):
            abort(401, message="Ongeldige API-key")

         api_key = api_key_header.split("Bearer ")[1]

         key_record = db.session.query(ApiKeys).filter_by(api_key=api_key).first()

         if not key_record:
            abort(401, message="Ongeldige API-key")

         g.key = {'key': key_record.api_key, 'company_id': key_record.company_id}

         return f(*args, **kwargs)

      return decorated_function

   return decorator
