from flask_app import DATABASE
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.model import user_model, type_model , workout_model





class UserWorkout:
    def __init__(self, data):
        self.id = data['id']
        self.user_id =data['user_id']
        self.workout_id = data['workout_id']
        self.created_at= data['created_at']
        self.updated_at = data['updated_at']
        self.user= None
        self.workout = None
        
        
    # @classmethod
    # def all_users_workouts(cls, data):
    #     query = """
    #     SELECT * FROM users_workouts JOIN users ON users.id = users_workouts.user_id
    #     JOIN workouts ON workouts.id= users_workouts.workout_id 
    #     JOIN typesof ON typesof.id = workouts.type_id WHERE users.id = %(id)s;
        
    #     """
    #     results = connectToMySQL(DATABASE).query_db(query, data)
    #     users_workouts =[]
    #     if results:
    #         workout = cls(results[0])
    #         for row in results:
                
        
        
        
        