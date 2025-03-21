from flask import g, request
from flask_restful import Resource, abort, fields, marshal_with
from sqlalchemy import asc, desc
import datetime
from backend import db
from backend.database.models import Research, LimitationsModel
from backend.utils.check_permissions import check_permission_rest


limitation_fields = {
    'limitation_id': fields.Integer,
    'limitation': fields.String
}

research_fields = {
    'research_id': fields.Integer,
    'title': fields.String,
    'is_available': fields.Boolean,
    'description': fields.String,
    'start_date': fields.String,
    'end_date': fields.String,
    'location': fields.String,
    'has_reward': fields.Boolean,
    'reward': fields.String,
    'target_min_age': fields.Integer,
    'target_max_age': fields.Integer,
    'status_id': fields.Integer,
    'research_type_id': fields.Integer,
    'limitations': fields.List(fields.Nested(limitation_fields))
}

paginated_research_fields = {
    'researches': fields.List(fields.Nested(research_fields)),
    'pagination': fields.Nested({
        'total_items': fields.Integer,
        'total_pages': fields.Integer,
        'current_page': fields.Integer,
        'items_per_page': fields.Integer
    })
}

class ResearchesRest(Resource):
    @check_permission_rest('admin')
    @marshal_with(paginated_research_fields)
    def get(self):
        sort_by = request.args.get('sort_by', 'research_id')
        sort_order = request.args.get('sort_order', 'asc').lower()

        if sort_order not in ['asc', 'desc']:
            abort(400, message="Invalid sort_order value. Use 'asc' or 'desc'.")

        sort_columns = {
            'research_id': Research.research_id,
            'title': Research.title,
            'start_date': Research.start_date,
            'end_date': Research.end_date,
            'location': Research.location,
            'status_id': Research.status_id
        }

        sort_column = sort_columns.get(sort_by)
        if not sort_column:
            abort(400, message=f"Invalid sort_by value. Valid options: {', '.join(sort_columns.keys())}")

        sort_direction = asc(sort_column) if sort_order == 'asc' else desc(sort_column)

        page = request.args.get('page', 1, type=int)
        max_entries_per_page = request.args.get('max_entries', 10, type=int)

        if max_entries_per_page <= 0:
            abort(400, message="max_entries must be greater than 0.")

        query = Research.query.order_by(sort_direction)

        pagination = query.paginate(page=page, per_page=max_entries_per_page, error_out=False)
        researches = pagination.items

        return {
            'researches': researches,
            'pagination': {
                'total_items': pagination.total,
                'total_pages': pagination.pages,
                'current_page': pagination.page,
                'items_per_page': pagination.per_page
            }
        }, 200

class SingleResearchRest(Resource):
    @check_permission_rest('admin')
    @marshal_with(research_fields)
    def get(self, research_id):
        research = Research.query.get(research_id)
        if not research:
            abort(404 , message=f"Onderzoek {research_id} bestaat niet.")
        return research, 200

    @check_permission_rest('admin')
    @marshal_with(research_fields)
    def patch(self, research_id):
        research = Research.query.get(research_id)
        if not research:
            abort(404, message="Onderzoek niet gevonden")

        data = request.get_json()

        research.title = data.get('title', research.title)
        research.is_available = data.get('is_available', research.is_available)
        research.description = data.get('description', research.description)


        start_date = data.get('start_date')
        if start_date:
            try:
                research.start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d').date()
            except ValueError:
                abort(400, message="Verkeerde begindatum, gebruik YYYY-MM-DD.")

        end_date = data.get('end_date')
        if end_date:
            try:
                research.end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d').date()
            except ValueError:
                abort(400, message="Verkeerde einddatum, gebruik YYYY-MM-DD.")

        research.location = data.get('location', research.location)
        research.has_reward = data.get('has_reward', research.has_reward)
        research.reward = data.get('reward', research.reward)
        research.target_min_age = data.get('target_min_age', research.target_min_age)
        research.target_max_age = data.get('target_max_age', research.target_max_age)
        research.status_id = data.get('status_id', research.status_id)
        research.research_type_id = data.get('research_type_id', research.research_type_id)


        limitation_ids = data.get('limitation_ids')
        if limitation_ids is not None:
            research.limitations.clear()

            limitations = LimitationsModel.query.filter(
                LimitationsModel.limitation_id.in_(limitation_ids)
            ).all()

            research.limitations.extend(limitations)

        try:
            db.session.commit()
        except Exception as exception:
            db.session.rollback()
            abort(500, message=f"updaten van onderzoek niet gelukt: {str(exception)}")
        return research, 200

    @check_permission_rest('admin')
    def delete(self, research_id):
        research = Research.query.get(research_id)
        if not research:
            abort(404, message="Onderzoek niet gevonden")
        try:
            db.session.delete(research)
            db.session.commit()
        except Exception as exception:
            db.session.rollback()
            abort(500, message=f"Verwijderen van onderzoek niet gelukt: {str(exception)}")

        return {'message': 'Onderzoek succesvol verwijderd.'}, 200

