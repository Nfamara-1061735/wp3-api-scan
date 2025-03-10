import datetime

from flask import Blueprint, jsonify
from flask_restful import Resource, Api, reqparse, fields, marshal_with, abort

from backend.api.login import Login
from backend.database.models.research_model import Research
from backend.database.models.limitations_model import LimitationsModel
from backend.database.models.peer_expert_registration_model import PeerExpertRegistration
from backend import db

api_bp = Blueprint('api', __name__)
api = Api(api_bp)


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
      args = research_args.parse_args()

      try:
         start_date = datetime.datetime.strptime(args['start_date'], '%d-%m-%Y').date()
         end_date = datetime.datetime.strptime(args['end_date'], '%d-%m-%Y').date()
      except ValueError:
         abort(400, message="Ongeldige datum. Gebruik DD-MM-YYYY.")

      single_research = Research.query.filter_by(research_id=research_id).first()
      if not single_research:
         abort(404, message="Onderzoek niet gevonden")

      #gets the info that is already there and then changes it with what you provide
      if args.get('title'):
         single_research.title = args['title']
      if args.get('is_available') is not None:
         single_research.is_available = args['is_available']
      if args.get('description'):
         single_research.description = args['description']
      if start_date:
         single_research.start_date = start_date
      if end_date:
         single_research.end_date = end_date
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
      if args.get('status_id'):
         single_research.status_id = args['status_id']
      if args.get('research_type_id'):
         single_research.research_type_id = args['research_type_id']

      if args.get('limitation_ids') is not None:
         single_research.limitations.clear()
         limitations = LimitationsModel.query.filter(LimitationsModel.limitation_id.in_(args['limitation_ids'])).all()
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

      if not filtered_researches:
         abort(404, message="Research(es) not found")

      formatted_researches = [
         {
            "research_id": research.research_id,
            "title": research.title,
            "is_available": research.is_available,
            "description": research.description,
            "start_date": research.start_date.strftime('%d-%m-%Y') if research.start_date else None,
            "end_date": research.end_date.strftime('%d-%m-%Y') if research.end_date else None,
            "location": research.location,
            "has_reward": research.has_reward,
            "reward": research.reward,
            "target_min_age": research.target_min_age,
            "target_max_age": research.target_max_age,
            "status_id": research.status_id,
            "research_type_id": research.research_type_id
         }
         for research in filtered_researches
      ]

      return jsonify(formatted_researches), 200

class FilteredPeerExpertRegistrations(Resource):
   @marshal_with(researchFields)
   def get(self, registration_status_id):
      registrations = PeerExpertRegistration.query.filter_by(registration_status_id=registration_status_id).all()

      if not registrations:
         abort(404, message="Registratie(s) niet gevonden.")

      return registrations

   @marshal_with(researchFields)
   def patch(self, peer_expert_registration_id, registration_status_id):
      args = registration_args.parse_args()

      single_registration = PeerExpertRegistration.query.filter_by(peer_expert_registration_id=peer_expert_registration_id).first()
      if not single_registration:
         abort(404, message="Registratie niet gevonden.")

      if args.get('registration_status_id'):
         single_registration.registration_status_id = registration_status_id


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
