import datetime

from flask import Blueprint
from flask_restful import Resource, Api, reqparse, fields, marshal_with, abort
from backend.database.models.research_model import Research
from backend import db

api_bp = Blueprint('api', __name__)
api = Api(api_bp)

research_args = reqparse.RequestParser()
research_args.add_argument('title', type=str, required=True, help="Title is required (name of the organisation)")
research_args.add_argument('is_available', type=bool, required=True, help="Availability status is required.")
research_args.add_argument('description', type=str, required=True, help="Description is required")
research_args.add_argument('start_date', type=str, required=True, help="Valid input is dd-mm-yyyy")
research_args.add_argument('end_date', type=str, required=True, help="Valid input is dd-mm-yyyy")
research_args.add_argument('location', type=str, required=True, help="Location is required")
research_args.add_argument('has_reward', type=bool, required=True, help="Reward status is required")
research_args.add_argument('reward', type=str)
research_args.add_argument('target_min_age', type=int)
research_args.add_argument('target_max_age', type=int)
research_args.add_argument('status_id', type=int, required=True, help="Status ID is required")
research_args.add_argument('research_type_id', type=int, required=True, help="Research Type ID is required")

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
   'research_type_id': fields.Integer
}

class Researches(Resource):
   @marshal_with(researchFields)
   def get(self):
      researches = Research.query.all()

      #this loops sets the dates to DD-MM-YYYY before returning 
      for research in researches:
         research.start_date = research.start_date.strftime('%d-%m-%Y')
         research.end_date = research.end_date.strftime('%d-%m-%Y')

      return researches, 200
   
   @marshal_with(researchFields)
   def post(self):
      args = research_args.parse_args()

      #This converts the dates from strings to date.datetime objects
      try:
         start_date = datetime.datetime.strptime(args['start_date'], '%d-%m-%Y').date()
         end_date = datetime.datetime.strptime(args['end_date'], '%d-%m-%Y').date()
      except ValueError:
         abort(400, message="Invalid date. Use DD-MM-YYYY.")
         return

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

      db.session.add(new_research)
      db.session.commit()

      return new_research, 201

class SingleResearch(Resource):
   @marshal_with(researchFields)
   def get(self, research_id):
      single_research = Research.query.filter_by(research_id=research_id).first()
      if not single_research:
         abort(404, message="Research not found")
      return single_research, 200

   @marshal_with(researchFields)
   def patch(self, research_id):
      args = research_args.parse_args()

      try:
         start_date = datetime.datetime.strptime(args['start_date'], '%d-%m-%Y').date()
         end_date = datetime.datetime.strptime(args['end_date'], '%d-%m-%Y').date()
      except ValueError:
         abort(400, message="Invalid date. Use DD-MM-YYYY.")
         return

      single_research = Research.query.filter_by(research_id=research_id).first()
      if not single_research:
         abort(404, message="Research not found")

      #gets the info that is already thare and then changes it with what you provide
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

      db.session.commit()

      return single_research, 200

   @marshal_with(researchFields)
   def delete(self, research_id):
      single_research = Research.query.filter_by(research_id=research_id).first()
      if not single_research:
         abort(404, message="Research not found")

      db.session.delete(single_research)
      db.session.commit()
      researches = Research.query.all()
      return researches, 200

api.add_resource(Researches, '/api/researches')
api.add_resource(SingleResearch, '/api/researches/<int:research_id>')



