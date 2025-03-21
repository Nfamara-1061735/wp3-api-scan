from functools import wraps
from typing import Optional

from flask import session, g, redirect, url_for
from flask_restful import abort

from backend.database.models import Users


# Helper functions
def get_user_from_session() -> Optional[dict[str, str]]:
    """Retrieve user session from the session."""
    return session.get('user')


def get_user_by_id(user_id: str):
    """Retrieve user from the database using the user ID."""
    return Users.query.get(user_id)


def check_user_permissions(user, role: str) -> bool:
    """Check if the user has the required permission based on their role."""
    if role == 'peer' and user.peer_expert_info:
        return True
    elif role == 'admin' and user.admin_info:
        return True
    return False


# Decorator functions

def check_permission(role: str):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            user_session = get_user_from_session()  # Get user session

            if not user_session:
                return f(*args, **kwargs)  # Return if user not logged in

            user_id = user_session.get('id')

            if not user_id:
                return 'Forbidden: Malformed user session', 403

            user = get_user_by_id(user_id)
            if not user:
                return f(*args, **kwargs)  # Return if user doesn't exist

            if check_user_permissions(user, role):  # Check if the user has the required role
                g.user = user  # Store the user object in flask.g
                return f(*args, **kwargs)  # User has required role, allow access
            else:
                return f(*args, **kwargs)  # Return

        return decorated_function

    return decorator


def check_permission_rest(role: Optional[str] = None):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            user_session = get_user_from_session()  # Get user session

            if not user_session:
                abort(403, message='Forbidden: No user logged in')  # No user logged in

            user_id = user_session.get('id')

            if not user_id:
                abort(403, message='Forbidden: Malformed user session')

            user = get_user_by_id(user_id)
            if not user:
                abort(403, message='Forbidden: User not found')  # User not found in the database

            # Check permissions
            if not role:
                g.user = user  # Store the user object in flask.g
                return f(*args, **kwargs)  # User is logged in, allow access
            elif check_user_permissions(user, role):  # Check if the user has the required role
                g.user = user  # Store the user object in flask.g
                return f(*args, **kwargs)  # User has required role, allow access
            else:
                abort(403, message=f'Forbidden: User does not have {role} permissions')  # Forbidden

        return decorated_function

    return decorator