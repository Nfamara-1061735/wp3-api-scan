from datetime import datetime
from flask import g, request
from flask_restful import Resource, abort
from flask_sqlalchemy.pagination import Pagination
from flask_sqlalchemy.query import Query
from sqlalchemy import asc, desc

from backend import db
from backend.database.models import PeerExperts, Users, PeerExpertsLimitations, PeerExpertsResearchTypes
from backend.utils.check_permissions import check_permission_rest


def flatten_peer_expert(expert: PeerExperts):
    return {
        'peer_expert_id': expert.peer_expert_id,
        'postal_code': expert.postal_code,
        'gender': expert.gender,
        'birth_date': expert.birth_date.isoformat() if expert.birth_date else None,
        'tools_used': expert.tools_used,
        'short_bio': expert.short_bio,
        'special_notes': expert.special_notes,
        'accepted_terms': expert.accepted_terms,
        'has_supervisor': expert.has_supervisor,
        'supervisor_or_guardian_name': expert.supervisor_or_guardian_name,
        'supervisor_or_guardian_email': expert.supervisor_or_guardian_email,
        'supervisor_or_guardian_phone': expert.supervisor_or_guardian_phone,
        'availability_notes': expert.availability_notes,
        'contact_preference_id': expert.contact_preference_id,
        'user_id': expert.user_id,
        'peer_expert_status_id': expert.peer_expert_status_id,
        'user': {
            'user_id': expert.user.user_id,
            'first_name': expert.user.first_name,
            'last_name': expert.user.last_name,
            'email': expert.user.email,
            'phone_number': expert.user.phone_number,
        },
        'limitations': [{
            'limitation_id': lim.limitation_id,
            'limitation': lim.limitation.limitation if lim.limitation else None
        } for lim in expert.limitations],
        'research_types': [{
            'research_type_id': rt.research_type_id
        } for rt in expert.research_types]
    }

# GET all peer experts (paginated + sorted)
class PeerExpertRest(Resource):
    @check_permission_rest()
    def get(self):
        sort_by = request.args.get('sort_by', 'peer_expert_id')
        sort_order = request.args.get('sort_order', 'asc').lower()

        if sort_order not in ['asc', 'desc']:
            abort(400, message="Invalid sort_order value. Use 'asc' or 'desc'.")

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

        sort_column = sort_columns.get(sort_by)
        if not sort_column:
            abort(400, message=f"Invalid sort_by value. Valid options: {', '.join(sort_columns.keys())}")

        sort_direction = asc(sort_column) if sort_order == 'asc' else desc(sort_column)

        page = request.args.get('page', 1, type=int)
        max_entries_per_page = request.args.get('max_entries', None, type=int)
        show_all = request.args.get('show_all', 'false').lower() == 'true'

        if max_entries_per_page is not None and max_entries_per_page <= 0:
            abort(400, message="max_entries_per_page must be greater than 0.")

        query: Query = None
        if g.user.admin_info:
            query = PeerExperts.query.join(Users).order_by(sort_direction)
        elif g.user.peer_expert_info:
            peer_id = g.user.peer_expert_info.peer_expert_id
            query = PeerExperts.query.filter_by(peer_expert_id=peer_id).join(Users).order_by(sort_direction)
        else:
            abort(403, message="Forbidden access")

        if not show_all:
            query = query.filter(PeerExperts.peer_expert_status_id != 4)

        if max_entries_per_page:
            pagination: Pagination = query.paginate(page=page, per_page=max_entries_per_page, error_out=False)
            peer_experts = pagination.items
        else:
            pagination = None
            peer_experts = query.all()

        peer_expert_list = [flatten_peer_expert(expert) for expert in peer_experts]

        return {
            'peer_experts': peer_expert_list,
            'pagination': {
                'total_items': pagination.total if pagination else len(peer_experts),
                'total_pages': pagination.pages if pagination else 1,
                'current_page': pagination.page if pagination else 1,
                'items_per_page': pagination.per_page if pagination else len(peer_experts)
            }
        }, 200

class SinglePeerExpertRest(Resource):
    @check_permission_rest()
    def get(self, peer_expert_id):
        peer_expert: PeerExperts = PeerExperts.query.get(peer_expert_id)

        if not peer_expert:
            abort(404, message="Peer expert not found")

        if g.user.admin_info or (
            g.user.peer_expert_info and g.user.peer_expert_info.peer_expert_id == peer_expert_id
        ):
            return flatten_peer_expert(peer_expert), 200

        abort(403, message="Forbidden: You don't have permission to view this peer expert.")

    @check_permission_rest('admin')
    def patch(self, peer_expert_id):
        peer_expert: PeerExperts = PeerExperts.query.get(peer_expert_id)

        if not peer_expert:
            abort(404, message="Peer expert not found")

        data = request.get_json()

        new_status_id = data.get('peer_expert_status_id')
        if new_status_id is None:
            abort(400, message="'peer_expert_status_id' is required.")

        try:
            peer_expert.peer_expert_status_id = new_status_id
            db.session.commit()
            return {'message': f"Peer expert status updated to {new_status_id}."}, 200
        except Exception:
            db.session.rollback()
            abort(500, message="Error updating peer expert status.")