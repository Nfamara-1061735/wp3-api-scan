import datetime
from flask_restful import Resource, Api, reqparse, fields, marshal_with, abort
from backend.database.models.research_model import Research
from backend import db


api = Api()

research_args = reqparse.RequestParser()
research_args.add_argument('title', type=str, required=True, help="Title is required (name of the organisation)")
research_args.add_argument('is_available', type=bool, required=True, help="Availibility status is required.")
research_args.add_argument('description', type=str, required=True, help="Description is required")
research_args.add_argument('start_date', type=str, required=True, help="Valid input is dd-mm-yyyy")
research_args.add_argument('end_date', type=str, required=True, help="Valid input is dd-mm-yyyy")
research_args.add_argument('location', type=str, required=True, help="Location is required")
research_args.add_argument('has_reward', type=bool, required=True, help="Reward status is required")
research_args.add_argument('reward', type=str)
research_args.add_argument('target_min_age', type=int)
research_args.add_argument('target_max_age', type=int)

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
   'target_max_age': fields.Integer
}

class Researches(Resource):
   @marshal_with(researchFields)
   def get(self):
      researches = Research.query.all()

      #this loops sets the dates to DD-MM-YYYY before returning 
      for research in researches:
         research.start_date = research.start_date.strftime('%d-%m-%Y')
         research.end_date = research.end_date.strftime('%d-%m-%Y')

      return researches
   
   @marshal_with(researchFields)
   def post(self):
      args = research_args.parse_args()

      #This converts the dates from strings to date.datetime objects
      try:
         start_date = datetime.datetime.strptime(args['start_date'], '%d-%m-%Y').date()
         end_date = datetime.datetime.strptime(args['end_date'], '%d-%m-%Y').date()
      except ValueError:
         abort(400, message="Invalid date. Use DD-MM-YYYY.")
         
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
         target_max_age = args['target_max_age']
      )

      db.session.add(new_research)
      db.session.commit()

      researches = Research.query.all()
      return researches, 201


api.add_resource(Researches, '/api/researches/')



