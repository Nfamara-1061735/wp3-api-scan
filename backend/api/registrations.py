from flask import session, g, request
from flask_restful import Resource, abort, fields, marshal_with

from backend import db
from backend.api.researches_api import researchFields
from backend.database.models import PeerExpertRegistration, Users, Research
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

        # Get the filter parameters from the query string
        filters = {
            'registration_status_id': request.args.get('registration_status_id', type=int),
            'research_id': request.args.get('research_id', type=int)
        }

        # Remove filters that are None (optional filters that were not provided)
        filters = {key: value for key, value in filters.items() if value is not None}

        if g.user.admin_info:
            # Start with the base query
            registrations_query = PeerExpertRegistration.query

            # Dynamically apply filters to the query
            for key, value in filters.items():
                registrations_query = registrations_query.filter_by(**{key: value})

            registrations = registrations_query.all()

        elif g.user.peer_expert_info:
            peer_id = g.user.peer_expert_info.peer_expert_id
            registrations_query = PeerExpertRegistration.query.filter_by(peer_expert_id=peer_id)

            # Dynamically apply filters for peer expert
            for key, value in filters.items():
                registrations_query = registrations_query.filter_by(**{key: value})

            registrations = registrations_query.all()

        return registrations, 200

    @check_permission_rest()
    @marshal_with(peer_expert_registration_fields)
    def post(self):
        data = request.get_json()

        peer_expert_id = None
        if g.user.peer_expert_info:
            peer_expert_id = g.user.peer_expert_info.peer_expert_id

        # Create new registration from the provided data
        new_registration = PeerExpertRegistration(
            peer_expert_id=peer_expert_id if peer_expert_id else data['peer_expert_id'],
            research_id=data['research_id'],
            registration_status_id=1  # 'nieuw' status by default
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
            print(registration_id)
            if registration.registration_status_id != 1:
                abort(403, message="Forbidden: You can only delete registrations with status ID 1.")
            if registration.peer_expert_id != g.user.peer_expert_info.peer_expert_id:
                abort(403, message="Forbidden: You can only delete your own registration.")

        # Admin can delete any registration
        if g.user.peer_expert_info or g.user.admin_info:
            db.session.delete(registration)
            db.session.commit()
            return '', 204  # No content to return, successfully deleted

        abort(403, message="Forbidden: You don't have permission to delete this registration.")


class ResearchesRegistrationState(Resource):
    @check_permission_rest('peer')
    @marshal_with(researchFields)
    def get(self):
        # Get the peer expert ID for the currently logged-in user
        peer_id = g.user.peer_expert_info.peer_expert_id

        # Get the 'state' query parameter to specify which type of research to fetch
        state = request.args.get('state', type=str)  # 'not_registered' or 'registered'

        # Get the list of research IDs the current peer expert is registered for
        registered_research_ids = db.session.query(PeerExpertRegistration.research_id).filter_by(
            peer_expert_id=peer_id).all()
        registered_research_ids = [research_id[0] for research_id in
                                   registered_research_ids]  # Flatten the list of tuples

        # Initialize the research query
        researches_query = Research.query

        # Apply filter based on the state
        if state == 'registered':
            if registered_research_ids:
                researches_query = researches_query.filter(Research.research_id.in_(registered_research_ids))
            else:
                # If the peer expert is not registered for anything, return an empty result
                researches_query = researches_query.filter(Research.research_id == None)  # No match found
        elif state == 'unregistered':
            if registered_research_ids:
                researches_query = researches_query.filter(Research.research_id.notin_(registered_research_ids))
        else:
            # If no valid state is provided, you can either return an error or all researches.
            return abort(400, message='Invalid state parameter. Use "registered" or "not_registered".')

        # Fetch the results
        researches = researches_query.all()

        return researches, 200
