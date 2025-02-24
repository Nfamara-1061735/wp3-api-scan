import datetime
from flask_restful import Resource, Api, reqparse, fields, marshal_with, abort
from backend.database.models.research_model import Research


api = Api()

user_args = reqparse.RequestParser()
user_args.add_argument('title', type=str, required=True)
user_args.add_argument('is_availeble', type=bool, required=True)
user_args.add_argument('description', type=str, required=True)
user_args.add_argument('start_date', type=str, required=True, help="Valid input is dd-mm-yyyy")
user_args.add_argument('end_date', type=str, required=True, help="Valid input is dd-mm-yyyy")
user_args.add_argument('location', type=str, required=True)
user_args.add_argument('has_reward', type=bool, required=True)
user_args.add_argument('reward', type=str)
user_args.add_argument('target_min_age', type=int)
user_args.add_argument('target_max_age', type=int)



class Researches(Resource):
   def get(self):
      researches = Research.query.all()
      return researches

api.add_resource(Researches, '/api/researches/')



