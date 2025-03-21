from functools import wraps

from flask import Blueprint, jsonify, request
from flask_restful import Resource, Api, reqparse, fields, marshal_with, abort

from backend import db
from backend.api.login import Login
from backend.api.peer_experts import PeerExpertRest, SinglePeerExpertRest
from backend.api.registrations import Registrations, Registration, ResearchesRegistrationState
from backend.api.researches_api import Researches, SingleResearch
from backend.api.researches_crud_api import ResearchesRest, SingleResearchRest
from backend.api.utils import method_not_allowed
from backend.database.models.api_keys_model import ApiKeys
from backend.database.models.limitations_model import LimitationsModel
from backend.database.models.peer_expert_registration_model import PeerExpertRegistration
from backend.database.models.peer_experts_model import PeerExperts

api_bp = Blueprint('api', __name__)
api = Api(api_bp)

limitationFields = {
   'limitation_id': fields.Integer,
   'limitation': fields.String
}

registration_args = reqparse.RequestParser()
registration_args.add_argument('peer_expert_registration_id', type=int, required=True, help="Peer Expert Registration ID is verplicht")
registration_args.add_argument('registration_status_id', type=int, required=True, help="Registration Status ID is verplicht")
registration_args.add_argument('peer_expert_id', type=int, required=False)
registration_args.add_argument('research_id', type=int, required=False)

registrationFields = {
   'peer_expert_registration_id': fields.Integer,
   'registration_status_id': fields.Integer,
   'peer_expert_id': fields.Integer,
   'research_id': fields.Integer,
}

peer_expert_args = reqparse.RequestParser()
peer_expert_args.add_argument('peer_expert_id', type=int, required=True)
peer_expert_args.add_argument('postal_code', type=str)
peer_expert_args.add_argument('gender', type=str)
peer_expert_args.add_argument('birth_date', type=str)
peer_expert_args.add_argument('tools_used', type=str)
peer_expert_args.add_argument('short_bio', type=str)
peer_expert_args.add_argument('special_notes', type=str)
peer_expert_args.add_argument('accepted_terms', type=bool)
peer_expert_args.add_argument('has_supervisor', type=bool)
peer_expert_args.add_argument('supervisor_or_guardian_name')
peer_expert_args.add_argument('availability_notes', type=str)
peer_expert_args.add_argument('contact_preference_id', type=int)
peer_expert_args.add_argument('user_id', type=int)
peer_expert_args.add_argument('peer_expert_status_id', type=int)

peerExpertFields = {
   'peer_expert_id': fields.Integer,
   'postal_code': fields.String,
   'gender': fields.String,
   'birth_date': fields.String,
   'tools_used': fields.String,
   'short_bio': fields.String,
   'special_notes': fields.String,
   'accepted_terms': fields.Boolean,
   'has_supervisor': fields.Boolean,
   'supervisor_or_guardian_name': fields.String,
   'availability_notes': fields.String,
   'contact_preference_id': fields.Integer,
   'user_id': fields.Integer,
   'peer_expert_status_id': fields.Integer
}

class FilteredPeerExpertRegistrations(Resource):
   @marshal_with(registrationFields)
   def get(self, registration_status_id):
      registrations = PeerExpertRegistration.query.filter_by(registration_status_id=registration_status_id).all()

      if not registrations:
         abort(404, message="Registratie(s) niet gevonden.")

      return registrations, 200

   @marshal_with(registrationFields)
   def patch(self, peer_expert_registration_id, registration_status_id):
      args = registration_args.parse_args()

      single_registration = PeerExpertRegistration.query.filter_by(peer_expert_registration_id=peer_expert_registration_id).first()
      if not single_registration:
         abort(404, message="Registratie niet gevonden.")

      if args.get('registration_status_id'):
         single_registration.registration_status_id = registration_status_id

      db.session.commit()
      return single_registration, 200

class FilteredPeerExperts(Resource):
   @marshal_with(peerExpertFields)
   def get(self, peer_expert_status_id):
      peer_experts = PeerExperts.query.filter_by(peer_expert_status_id=peer_expert_status_id).all()

      if not peer_experts:
         abort(404, message="Registratie(s) niet gevonden.")

      return peer_experts, 200

class Limitations(Resource):
   @marshal_with(limitationFields)
   def get(self):
      limitations = LimitationsModel.query.all()
      return limitations, 200

   def post(self):
      return method_not_allowed()

   def put(self):
      return method_not_allowed()

   def patch(self):
      return method_not_allowed()

   def delete(self):
      return method_not_allowed()

api.add_resource(Researches, '/researches/')
api.add_resource(FilteredPeerExperts, '/peer_experts/')
api.add_resource(FilteredPeerExpertRegistrations, '/peer_expert_registrations/')
api.add_resource(SingleResearch, '/researches/<int:research_id>/')
api.add_resource(ResearchesRegistrationState, '/researches/registration-state')
api.add_resource(Limitations, '/limitations/')
api.add_resource(Login, '/login')
api.add_resource(PeerExpertRest, '/peers')
api.add_resource(SinglePeerExpertRest, '/peers/<int:peer_expert_id>')
api.add_resource(Registrations, '/peers/registrations')
api.add_resource(Registration, '/peers/registrations/<int:registration_id>')
api.add_resource(ResearchesRest, '/researches-admin')
api.add_resource(SingleResearchRest, '/researches-admin/<int:research_id>')