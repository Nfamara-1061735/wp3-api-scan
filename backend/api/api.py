import datetime

from flask import Blueprint, jsonify, request, render_template
from flask_restful import Resource, Api, reqparse, fields, marshal_with, abort

from backend.api.login import Login
from backend.database.models.research_model import Research
from backend.database.models.limitations_model import LimitationsModel
from backend.database.models.api_keys_model import ApiKeys
from backend.database.models.peer_expert_registration_model import PeerExpertRegistration
from backend.database.models.peer_experts_model import PeerExperts
from backend import db
from functools import wraps

api_bp = Blueprint('api', __name__)
api = Api(api_bp)


#api-key validatie
def require_api_key(f):
   @wraps(f)
   def decorated_function(*args, **kwargs):
      api_key = request.headers.get("Authorization")

      if not api_key or not api_key.startswith("Bearer "):
         return jsonify({"error": "API-key ontbreekt of onjuist formaat"}), 401  # JSON-error

      api_key = api_key.split("Bearer ")[1]

      if not db.session.query(ApiKeys).filter_by(api_key=api_key).first():
         return jsonify({"error": "Ongeldige API-key"}), 401  # JSON-error

      return f(*args, **kwargs)  #Als API-key geldig is wordt de functie pas uitgevoerd

   return decorated_function


def method_not_allowed():
   response = jsonify({"error": "Methode niet toegestaan"})
   response.status_code = 405
   return response

research_args = reqparse.RequestParser()
research_args.add_argument('title', type=str, required=True, help="Title is verplicht (naam van je organisatie)")
research_args.add_argument('is_available', type=bool, required=True, help="is_available is verplicht.")
research_args.add_argument('description', type=str, required=True, help="description is verplicht")
research_args.add_argument('start_date', type=str, required=True, help="Geldige invoer is dd-mm-yyyy")
research_args.add_argument('end_date', type=str, required=True, help="Geldige invoer is dd-mm-yyyy")
research_args.add_argument('location', type=str, required=True, help="location is verplicht")
research_args.add_argument('has_reward', type=bool, required=True, help="has_reward is verplicht")
research_args.add_argument('reward', type=str)
research_args.add_argument('target_min_age', type=int)
research_args.add_argument('target_max_age', type=int)
research_args.add_argument('status_id', type=int, required=True, help="Status ID is verplicht")
research_args.add_argument('research_type_id', type=int, required=True, help="Research Type ID is verplicht")
research_args.add_argument('limitation_ids', type=int, action='append', required=False, help="Een list van limitations ID's (voorbeeld [1, 2, 3])")

patch_research_args = reqparse.RequestParser()
patch_research_args.add_argument('status_id', type=int, required=False)
patch_research_args.add_argument('title', type=str, required=False)
patch_research_args.add_argument('is_available', type=bool, required=False)
patch_research_args.add_argument('description', type=str, required=False)
patch_research_args.add_argument('start_date', type=str, required=False)
patch_research_args.add_argument('end_date', type=str, required=False)
patch_research_args.add_argument('location', type=str, required=False)
patch_research_args.add_argument('has_reward', type=bool, required=False)
patch_research_args.add_argument('reward', type=str, required=False)
patch_research_args.add_argument('target_min_age', type=int, required=False)
patch_research_args.add_argument('target_max_age', type=int, required=False)
patch_research_args.add_argument('research_type_id', type=int, required=False)
patch_research_args.add_argument('limitation_ids', type=int, action='append', required=False)

researchFields = {
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
   'limitations': fields.List(fields.Nested({
      'limitation_id': fields.Integer,
      'limitation': fields.String
   }))
}

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

class Researches(Resource):
   @marshal_with(researchFields)
   def get(self):
      researches = Research.query.all()
      return researches, 200
   
   @marshal_with(researchFields)
   def post(self):
      args = research_args.parse_args()

      #This converts the dates from strings to date.datetime objects
      try:
         start_date = datetime.datetime.strptime(args['start_date'], '%d-%m-%Y').date()
         end_date = datetime.datetime.strptime(args['end_date'], '%d-%m-%Y').date()
      except ValueError:
         abort(400, message="Ongeldige datum. Gebruik DD-MM-YYYY.")

      new_research = Research(
         title = args['title'],
         is_available = args['is_available'],
         description = args['description'],
         start_date = start_date,
         end_date = end_date,
         location = args['location'],
         has_reward = args['has_reward'],
         reward = args['reward'],
         target_min_age = args['target_min_age'],
         target_max_age = args['target_max_age'],
         status_id = args['status_id'],
         research_type_id = args['research_type_id']
      )

      if args['limitation_ids']:
         limitations = LimitationsModel.query.filter(LimitationsModel.limitation_id.in_(args['limitation_ids'])).all()
         new_research.limitations.extend(limitations)

      db.session.add(new_research)
      db.session.commit()

      return new_research, 201

   def put(self):
      return method_not_allowed()

   def patch(self):
      return method_not_allowed()

   def delete(self):
      return method_not_allowed()

class SingleResearch(Resource):
   @marshal_with(researchFields)
   def get(self, research_id):
      single_research = Research.query.filter_by(research_id=research_id).first()
      if not single_research:
         abort(404, message="Onderzoek niet gevonden.")
      return single_research, 200

   @marshal_with(researchFields)
   def patch(self, research_id):
      args = patch_research_args.parse_args()

      single_research = Research.query.filter_by(research_id=research_id).first()
      if not single_research:
         abort(404, message="Onderzoek niet gevonden")

      if args.get('title'):
         single_research.title = args['title']
      if args.get('is_available') is not None:
         single_research.is_available = args['is_available']
      if args.get('description'):
         single_research.description = args['description']

      if args.get('start_date'):
         try:
            single_research.start_date = datetime.datetime.strptime(args['start_date'], '%d-%m-%Y').date()
         except ValueError:
            abort(400, message="Ongeldige startdatum. Gebruik DD-MM-YYYY.")

      if args.get('end_date'):
         try:
            single_research.end_date = datetime.datetime.strptime(args['end_date'], '%d-%m-%Y').date()
         except ValueError:
            abort(400, message="Ongeldige einddatum. Gebruik DD-MM-YYYY.")

      if args.get('location'):
         single_research.location = args['location']
      if args.get('has_reward') is not None:
         single_research.has_reward = args['has_reward']
      if args.get('reward'):
         single_research.reward = args['reward']
      if args.get('target_min_age') is not None:
         single_research.target_min_age = args['target_min_age']
      if args.get('target_max_age') is not None:
         single_research.target_max_age = args['target_max_age']
      if args.get('status_id') is not None:
         single_research.status_id = args['status_id']
      if args.get('research_type_id'):
         single_research.research_type_id = args['research_type_id']

      if args.get('limitation_ids') is not None:
         single_research.limitations.clear()
         limitations = LimitationsModel.query.filter(
            LimitationsModel.limitation_id.in_(args['limitation_ids'])
         ).all()
         single_research.limitations.extend(limitations)

      db.session.commit()
      return single_research, 200


   def delete(self, research_id):
      single_research = Research.query.filter_by(research_id=research_id).first()
      if not single_research:
         abort(404, message="Onderzoek niet gevonden.")

      db.session.delete(single_research)
      db.session.commit()
      return {"message": "Onderzoek succesvol verwijderd."}, 200

   def post(self):
      return method_not_allowed()

   def put(self):
      return method_not_allowed()

class FilteredResearch(Resource):
   @marshal_with(researchFields)
   def get(self, status_id):
      filtered_researches = Research.query.filter_by(status_id=status_id).all()

      return filtered_researches, 200

   @marshal_with(researchFields)
   def patch(self, new_status_id, research_id):
      args = research_args.parse_args()

      single_research = Research.query.filter_by(research_id=research_id).first()
      if not single_research:
         abort(404, message="Onderzoek niet gevonden")

      if args.get('status_id'):
         single_research.status_id = new_status_id

      db.session.commit()
      return single_research, 200

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
api.add_resource(SingleResearch, '/researches/<int:research_id>/')
api.add_resource(Limitations, '/limitations/')
api.add_resource(Login, '/login')
