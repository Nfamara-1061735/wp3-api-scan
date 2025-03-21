from flask_restful import Resource, fields, marshal_with

from backend.database.models import LimitationsModel, PeerExpertStatus, ContactPreferences, ResearchTypesModel

# Fields for serializing the ContactPreferences class to json for output
contact_preferences_fields = {
    'contact_preference_id': fields.Integer,
    'type': fields.String
}

# Fields for serializing the PeerExpertStatus class to json for output
peer_expert_status_fields = {
    'peer_expert_status_id': fields.Integer,
    'status': fields.String
}

# Fields for serializing the LimitationsModel class to json for output
limitations_fields = {
    'limitation_id': fields.Integer,
    'limitation': fields.String,
    'limitation_category': fields.String
}

# Fields for serializing the LimitationsModel class to json for output
research_type_fields = {
    'research_type_id': fields.Integer,
    'type': fields.String
}


class ContactPreferencesRest(Resource):
    @marshal_with(contact_preferences_fields)
    def get(self):
        return ContactPreferences.query.all()


class PeerExpertStatusRest(Resource):
    @marshal_with(peer_expert_status_fields)
    def get(self):
        return PeerExpertStatus.query.all()


class LimitationsRest(Resource):
    @marshal_with(limitations_fields)
    def get(self):
        return LimitationsModel.query.all(), 200


class ResearchTypesRest(Resource):
    @marshal_with(research_type_fields)
    def get(self):
        return ResearchTypesModel.query.all(), 200
