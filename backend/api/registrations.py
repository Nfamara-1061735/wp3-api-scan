from flask import session, g, request
from flask_restful import Resource, abort, fields, marshal_with

from backend import db
from backend.database.models import PeerExpertRegistration, Users
from backend.utils.check_permissions import check_permission_rest

peer_expert_registration_fields = {
    'peer_expert_registration_id': fields.Integer,
    'registration_status_id': fields.Integer,
    'peer_expert_id': fields.Integer,
    'research_id': fields.Integer,
    'registration_status': fields.Nested({
        'registration_status_id': fields.Integer,
        'status': fields.String
    })
}

class Registrations(Resource):
    @check_permission_rest()
    @marshal_with(peer_expert_registration_fields)
    def get(self):
        registrations: list[PeerExpertRegistration] = []

        # Get the status filter from the query parameters (if provided)
        registration_status_id = request.args.get('registration_status_id', type=int)

        if g.user.admin_info:
            if registration_status_id:
                # If a status filter is provided, filter by registration_status_id
                registrations = PeerExpertRegistration.query.filter_by(
                    registration_status_id=registration_status_id).all()
            else:
                # No filter provided, get all registrations
                registrations = PeerExpertRegistration.query.all()

        elif g.user.peer_expert_info:
            peer_id = g.user.peer_expert_info.peer_expert_id
            registrations_query = PeerExpertRegistration.query.filter_by(peer_expert_id=peer_id)

            if registration_status_id:
                # Apply status filter for peer expert as well
                registrations_query = registrations_query.filter_by(registration_status_id=registration_status_id)

            registrations = registrations_query.all()
        return registrations, 200

    @check_permission_rest()
    @marshal_with(peer_expert_registration_fields)
    def post(self):
        # Only admin can create new registrations
        if not g.user.admin_info:
            abort(403, message="Forbidden: Only admins can create registrations.")

        # Assuming you are receiving data in the request
        data = request.get_json()

        # Create new registration from the provided data
        new_registration = PeerExpertRegistration(
            peer_expert_id=data['peer_expert_id'],
            research_id=data['research_id'],
            registration_status_id=data['registration_status_id']
        )

        # Add to the database
        db.session.add(new_registration)
        db.session.commit()

        return new_registration, 201


class Registration(Resource):
    @check_permission_rest()
    @marshal_with(peer_expert_registration_fields)
    def get(self, registration_id):
        registration = PeerExpertRegistration.query.get(registration_id)

        if not registration:
            print('not found')
            abort(404, message="Registration not found")

        if g.user.admin_info:
            return registration, 200
        elif g.user.peer_expert_info:
            if registration.peer_expert_id == g.user.peer_expert_info.peer_expert_id:
                return registration, 200
            else:
                abort(403, message="Forbidden: You can only view your own registration.")
        else:
            abort(403, message="Forbidden: You don't have permission to view this registration.")

    @check_permission_rest()
    @marshal_with(peer_expert_registration_fields)
    def patch(self, registration_id):
        registration = PeerExpertRegistration.query.get(registration_id)

        if not registration:
            abort(404, message="Registration not found")

        # Peer experts are not allowed to modify registration details
        if g.user.peer_expert_info and not g.user.admin_info:
            abort(403, message="Forbidden: Peer experts cannot patch registrations.")

        # Admin can patch registration details
        if g.user.admin_info:
            data = request.get_json()
            registration.registration_status_id = data.get('registration_status_id',
                                                           registration.registration_status_id)
            registration.peer_expert_id = data.get('peer_expert_id', registration.peer_expert_id)
            registration.research_id = data.get('research_id', registration.research_id)

            db.session.commit()
            return registration, 200

        abort(403, message="Forbidden: You don't have permission to patch this registration.")

    @check_permission_rest()
    def delete(self, registration_id):
        registration = PeerExpertRegistration.query.get(registration_id)

        if not registration:
            abort(404, message="Registration not found")

        # Peer experts can only delete the registration if registration_status_id is 1 ('nieuw')
        if g.user.peer_expert_info:
            if registration.registration_status_id != 1:
                abort(403, message="Forbidden: You can only delete registrations with status ID 1.")
            if registration.peer_expert_id != g.user.peer_expert_info.peer_expert_id:
                abort(403, message="Forbidden: You can only delete your own registration.")

        # Admin can delete any registration
        if g.user.admin_info:
            db.session.delete(registration)
            db.session.commit()
            return '', 204  # No content to return, successfully deleted

        abort(403, message="Forbidden: You don't have permission to delete this registration.")
