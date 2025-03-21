from datetime import datetime

from flask import g, request
from flask_restful import Resource, abort, fields, marshal_with
from flask_sqlalchemy.pagination import Pagination
from flask_sqlalchemy.query import Query
from sqlalchemy import asc, desc

from backend import db
from backend.database.models import PeerExperts, Users, PeerExpertsLimitations, ResearchTypesModel, \
    PeerExpertsResearchTypes
from backend.database.models.peer_expert_research_type_model import PeerExpertResearchTypeModel
from backend.utils.check_permissions import check_permission_rest
from backend.utils.password import generate_salt, hash_password

# Fields for serializing the PeerExperts class to json for output (without pagination)
peer_experts_fields = {
    'peer_expert_id': fields.Integer,
    'postal_code': fields.String,
    'gender': fields.String,
    'birth_date': fields.DateTime('iso8601'),
    'tools_used': fields.String,
    'short_bio': fields.String,
    'special_notes': fields.String,
    'accepted_terms': fields.Boolean,
    'has_supervisor': fields.Boolean,
    'supervisor_or_guardian_name': fields.String,
    'supervisor_or_guardian_email': fields.String,
    'supervisor_or_guardian_phone': fields.String,
    'availability_notes': fields.String,
    'contact_preference_id': fields.Integer,
    'user_id': fields.Integer,
    'peer_expert_status_id': fields.Integer,
    'user': fields.Nested({
        'user_id': fields.Integer,
        'first_name': fields.String,
        'last_name': fields.String,
        'email': fields.String,
        'phone_number': fields.String,
    }),
    'limitations': fields.List(fields.Nested({
        'limitation_id': fields.Integer,
    })),
    'research_types': fields.List(fields.Nested({
        'research_type_id': fields.Integer,
    })),
}

# Fields for serializing the PeerExperts class to json for output (with pagination)
paginated_peer_experts_fields = {
    'peer_experts': fields.List(fields.Nested(peer_experts_fields)),
    'pagination': fields.Nested({
        'total_items': fields.Integer,
        'total_pages': fields.Integer,
        'current_page': fields.Integer,
        'items_per_page': fields.Integer
    })
}


class PeerExpertRest(Resource):
    @check_permission_rest()
    @marshal_with(paginated_peer_experts_fields)
    def get(self):
        # Get the sort_by parameter from the request query string (e.g., ?sort_by=postal_code)
        sort_by = request.args.get('sort_by', 'peer_expert_id')  # Default sort by peer_expert_id
        sort_order = request.args.get('sort_order', 'asc').lower()  # Default sort order is ascending

        # Validate sort_order to prevent SQL injection
        if sort_order not in ['asc', 'desc']:
            abort(400, message="Invalid sort_order value. Use 'asc' or 'desc'.")

        # Mapping of column names to model attributes
        sort_columns = {
            'peer_expert_id': PeerExperts.peer_expert_id,
            'postal_code': PeerExperts.postal_code,
            'gender': PeerExperts.gender,
            'birth_date': PeerExperts.birth_date,
            'tools_used': PeerExperts.tools_used,
            'short_bio': PeerExperts.short_bio,
            'special_notes': PeerExperts.special_notes,
            'accepted_terms': PeerExperts.accepted_terms,
            'has_supervisor': PeerExperts.has_supervisor,
            'availability_notes': PeerExperts.availability_notes,
            'contact_preference_id': PeerExperts.contact_preference_id,
            'user_id': PeerExperts.user_id,
            'peer_expert_status_id': PeerExperts.peer_expert_status_id,
            'first_name': Users.first_name,
            'last_name': Users.last_name
        }

        # Use the sort_by parameter to get the corresponding column for sorting
        sort_column = sort_columns.get(sort_by)

        if not sort_column:
            abort(400, message=f"Invalid sort_by value. Valid options: {', '.join(sort_columns.keys())}")

        # Determine the sort direction (ascending or descending)
        sort_direction = asc(sort_column) if sort_order == 'asc' else desc(sort_column)

        # Get the optional pagination parameters from the request query string
        page = request.args.get('page', 1, type=int)  # Default page is 1
        max_entries_per_page: int | None = request.args.get('max_entries', None,
                                                            type=int)  # Default is None (i.e., show all entries)

        # Get the show_all parameter (defaults to False)
        show_all = request.args.get('show_all', 'false').lower() == 'true'

        if max_entries_per_page is not None and max_entries_per_page <= 0:
            abort(400, message="max_entries_per_page must be greater than 0.")

        # Query the database and apply sorting
        query: Query | None = None
        if g.user.admin_info:
            query = PeerExperts.query.join(Users).order_by(sort_direction)
        elif g.user.peer_expert_info:
            peer_id = g.user.peer_expert_info.peer_expert_id
            query = PeerExperts.query.filter_by(peer_expert_id=peer_id).join(Users).order_by(sort_direction)
        else:
            abort(403, message="Forbidden access")

        # Exclude peer_expert_status_id of 4 unless show_all is True
        if not show_all:
            query = query.filter(PeerExperts.peer_expert_status_id != 4)

        # Pagination logic
        if max_entries_per_page:
            pagination: Pagination = query.paginate(page=page, per_page=max_entries_per_page, error_out=False)
            peer_experts = pagination.items
        else:
            pagination: None = None
            peer_experts = query.all()  # Show all entries if no pagination

        # Pagination return data
        total_items = pagination.total if pagination else len(peer_experts)
        total_pages = pagination.pages if pagination else 1
        current_page = pagination.page if pagination else 1
        items_per_page = pagination.per_page if pagination else total_items

        return {
            'peer_experts': peer_experts,
            'pagination': {
                'total_items': total_items,
                'total_pages': total_pages,
                'current_page': current_page,
                'items_per_page': items_per_page
            }
        }, 200

    @check_permission_rest('admin')
    def post(self):
        # Get data from the request
        data = request.get_json()

        # Validate required fields
        required_fields = ['postal_code', 'gender', 'birth_date', 'tools_used', 'short_bio', 'availability_notes',
                           'contact_preference_id', 'user_id', 'peer_expert_status_id']
        for field in required_fields:
            if field not in data:
                abort(400, message=f"'{field}' is required.")

        # Create a new PeerExpert instance from the request data
        peer_expert = PeerExperts(
            postal_code=data['postal_code'],
            gender=data['gender'],
            birth_date=datetime.strptime(data['birth_date'], '%Y-%m-%d'),
            tools_used=data.get('tools_used', None),
            short_bio=data['short_bio'],
            special_notes=data.get('special_notes', None),
            accepted_terms=data.get('accepted_terms', False),
            has_supervisor=data.get('has_supervisor', False),
            supervisor_or_guardian_name=data.get('supervisor_or_guardian_name', None),
            availability_notes=data['availability_notes'],
            contact_preference_id=data['contact_preference_id'],
            user_id=data['user_id'],
            peer_expert_status_id=data['peer_expert_status_id']
        )

        # Add the new PeerExpert to the database
        db.session.add(peer_expert)
        db.session.commit()

        return peer_expert, 201


class SinglePeerExpertRest(Resource):
    @check_permission_rest()
    @marshal_with(peer_experts_fields)
    def get(self, peer_expert_id):
        peer_expert: PeerExperts | None = PeerExperts.query.get(peer_expert_id)

        if not peer_expert:
            print('not found')
            abort(404, message="Peer expert not found")

        if g.user.admin_info:
            return peer_expert, 200
        elif g.user.peer_expert_info:
            if peer_expert.peer_expert_id == g.user.peer_expert_info.peer_expert_id:
                return peer_expert, 200
            else:
                abort(403, message="Forbidden: You can only view yourself.")
        abort(403, message="Forbidden: You don't have permission to view this peer expert.")

    @check_permission_rest()
    @marshal_with(peer_experts_fields)
    def patch(self, peer_expert_id):
        with db.session.no_autoflush:
            peer_expert: PeerExperts | None = PeerExperts.query.get(peer_expert_id)

            if not peer_expert:
                abort(404, message="Peer expert not found")

            # Check if the user is an admin or the peer expert themselves
            if g.user.admin_info or (
                    g.user.peer_expert_info and g.user.peer_expert_info.peer_expert_id == peer_expert_id):
                # Get data from the request
                data = request.get_json()

                # Update only the fields provided in the request using data.get()
                peer_expert.postal_code = data.get('postal_code', peer_expert.postal_code)
                peer_expert.gender = data.get('gender', peer_expert.gender)

                # Parse birth date
                birth_date_str = data.get('birth_date')
                if birth_date_str:
                    peer_expert.birth_date = datetime.strptime(birth_date_str, '%Y-%m-%d')

                peer_expert.tools_used = data.get('tools_used', peer_expert.tools_used)
                peer_expert.short_bio = data.get('short_bio', peer_expert.short_bio)
                peer_expert.special_notes = data.get('special_notes', peer_expert.special_notes)
                peer_expert.accepted_terms = data.get('accepted_terms', peer_expert.accepted_terms)
                peer_expert.has_supervisor = data.get('has_supervisor', peer_expert.has_supervisor)
                peer_expert.supervisor_or_guardian_name = data.get('supervisor_or_guardian_name',
                                                                   peer_expert.supervisor_or_guardian_name)
                peer_expert.availability_notes = data.get('availability_notes', peer_expert.availability_notes)
                peer_expert.contact_preference_id = data.get('contact_preference_id', peer_expert.contact_preference_id)

                if g.user.admin_info:
                    peer_expert.peer_expert_status_id = data.get('peer_expert_status_id',
                                                                 peer_expert.peer_expert_status_id)

                # Handle updates to the nested "user" object
                user_data = data.get('user')
                if user_data:
                    user: Users = peer_expert.user  # Assuming the peer_expert already has a related user
                    if user:
                        user.first_name = user_data.get('first_name', user.first_name)
                        user.last_name = user_data.get('last_name', user.last_name)
                        user.email = user_data.get('email', user.email)
                        user.phone_number = user_data.get('phone_number', user.phone_number)
                        if 'password' in user_data:
                            salt = generate_salt()
                            user.password = hash_password(user_data['password'], salt)
                            user.salt = salt

                # Handle updates to the "limitations" list
                limitations_data = data.get('limitations')
                if limitations_data is not None:
                    # Clear existing limitations
                    peer_expert.limitations = []

                    # Add the new limitations
                    for limitation in limitations_data:
                        limitation_id = limitation.get('limitation_id')
                        if limitation_id:
                            limitation_entry = PeerExpertsLimitations(peer_expert_id=peer_expert.peer_expert_id,
                                                                      limitation_id=limitation_id)
                            peer_expert.limitations.append(limitation_entry)

                # Handle updates to the "research_types" list
                research_types_data = data.get('research_types')
                if research_types_data is not None:
                    # Clear existing research types
                    peer_expert.research_types = []

                    # Add the new research types
                    for research_type in research_types_data:
                        research_type_id = research_type.get('research_type_id')
                        if research_type_id:
                            research_type_entry = PeerExpertsResearchTypes(peer_expert_id=peer_expert.peer_expert_id,
                                                                           research_type_id=research_type_id)
                            peer_expert.research_types.append(research_type_entry)

                # Commit the updates to the database
                db.session.commit()

                return peer_expert, 200  # Return the updated peer_expert with HTTP 200 status
            else:
                abort(403, message="Forbidden: You can only update your own registration.")

    @check_permission_rest()
    @marshal_with(peer_experts_fields)
    def delete(self, peer_expert_id):
        peer_expert: PeerExperts | None = PeerExperts.query.get(peer_expert_id)

        if not peer_expert:
            abort(404, message="Peer expert not found")

        # Check if the user is an admin or the peer expert themselves
        if g.user.admin_info or (g.user.peer_expert_info and g.user.peer_expert_info.peer_expert_id == peer_expert_id):
            # Set peer_expert_status_id to 4 ('gesloten')
            peer_expert.peer_expert_status_id = 4

            # Commit the changes to the database
            db.session.commit()

            return {'message': 'Peer expert deleted successfully.'}, 200  # Return a success message
        else:
            abort(403, message="Forbidden: You can only delete your own registration.")
