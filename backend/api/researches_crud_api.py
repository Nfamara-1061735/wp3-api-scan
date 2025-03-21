from flask import g, request
from flask_restful import Resource, abort, fields, marshal_with
from sqlalchemy import asc, desc
from backend import db
from backend.database.models import Research
from backend.utils.check_permissions import check_permission_rest


research_fields = {
    'research_id': fields.Integer,
    'title': fields.String,
    'description': fields.String,
    'start_date': fields.DateTime('iso8601'),
    'end_date': fields.DateTime('iso8601'),
    'location': fields.String,
    'status_id': fields.Integer,
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