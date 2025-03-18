from functools import wraps

from flask import session, g, redirect, url_for
from flask_restful import abort

from backend.database.models import Users


def check_permission(role: str):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            user_id = session.get('user')  # Get user ID from session

            if not user_id:
                return f(*args, **kwargs)  # Return if user not logged in

            user = Users.query.get(user_id)
            if not user:
                return f(*args, **kwargs)  # Return if user doesn't exist

            # Check if the user has the required property based on the role
            if role == 'peer' and user.peer_expert_info:
                g.user = user  # Store the user object in flask.g
                return f(*args, **kwargs)  # User has 'peer_expert_info', allow access
            elif role == 'admin' and user.admin_info:
                g.user = user  # Store the user object in flask.g
                return f(*args, **kwargs)  # User has 'admin_info', allow access
            else:
                return f(*args, **kwargs)  # Return

        return decorated_function

    return decorator


def check_permission_rest(role: str | None = None):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            user_id = session.get('user')  # Get user ID from session

            if not user_id:
                abort(403, message='Forbidden: No user logged in')  # No user logged in

            user: Users = Users.query.get(user_id)
            if not user:
                abort(403, message='Forbidden: User not found')  # User not found in the database

            # Check if the user has the required property based on the role
            if not role:
                g.user = user  # Store the user object in flask.g
                return f(*args, **kwargs)  # User is logged in, allow access
            elif role == 'peer' and user.peer_expert_info:
                g.user = user  # Store the user object in flask.g
                return f(*args, **kwargs)  # User has 'peer_expert_info', allow access
            elif role == 'admin' and user.admin_info:
                g.user = user  # Store the user object in flask.g
                return f(*args, **kwargs)  # User has 'admin_info', allow access
            else:
                abort(403, message=f'Forbidden: User does not have {role} permissions')  # Forbidden

        return decorated_function

    return decorator
