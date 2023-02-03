from flask_app import DATABASE
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.model import user_model, type_model




class Workout:
    def __init__(self, data):
        self.id = data['id']
        self.workout_name = data['workout_name']
        self.sets = data['sets']
        self.reps = data['reps']
        self.pounds = data['pounds']
        self.completed = data['completed']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.type_id = data['type_id']
        self.creator_id = data['creator_id']
        self.type = None
        self.creator = None
        
        
        
        
    
    

    
    @classmethod
    def edit(cls, data):
        query = '''
            UPDATE workouts SET workout_name = %(workout_name)s, sets = %(sets)s, reps = %(reps)s , pounds = %(pounds)s  WHERE id = %(id)s;

        '''
        return connectToMySQL(DATABASE).query_db(query, data)
    
    @classmethod
    def save(cls, data):
       
            
            query = '''
            INSERT INTO workouts (workout_name , sets, reps, pounds, completed, type_id,  creator_id) VALUES (%(workout_name)s,%(sets)s  , %(reps)s, %(pounds)s, %(completed)s, %(type_id)s,%(creator_id)s );
            '''
            return connectToMySQL(DATABASE).query_db(query, data)
    
    
    @classmethod
    def get_one(cls, data):
        query= '''
            SELECT * FROM workouts  
            JOIN typesof ON typesof.id= workouts.type_id;
        '''
        results = connectToMySQL(DATABASE).query_db(query, data)
        one_report=cls(results[0])
        for row in results:
            data ={
                **row,
                'id': row['users.id'],
                'created_at': row['users.created_at'],
                'updated_at': row['users.updated_at']
            }
            users_report = user_model.User(data)
            one_report.reporter = users_report
        return one_report
        
    @classmethod
    def delete(cls, data):
            query = "DELETE FROM workouts WHERE id = %(id)s;"
            return connectToMySQL(DATABASE).query_db(query, data)
        
    @staticmethod
    def validate_report(workout):
        is_valid = True
        if len(workout['workout_name']) < 3:
            is_valid = False
            flash("Must choose workout","report")
        if len(workout['sets']) < 3:
            is_valid = False
            flash("Amount of sets must be Chosen","report")
        if workout['reps'] == '':
            is_valid = False
            flash("Amount of reps must be chosen","report")
        if workout['pounds'] == "" :
            is_valid = False
            flash("Please enter how many pounds","report")
        
        if workout['completed'] == "" :
            is_valid = False
            flash("Please enter how many reports","report")
        
            
        return is_valid