from flask_app import DATABASE
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re 
from flask_app import app
from flask_app.model import workout_model, type_model
from flask_bcrypt import Bcrypt        
bcrypt = Bcrypt(app) 
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
NAME_REGEX = re.compile(r'^[a-zA-Z]+$')



class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at= data['created_at']
        self.updated_at = data['updated_at']
        self.my_workouts = []
        
    
    @classmethod
    def save(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s , %(password)s);"
        return connectToMySQL(DATABASE).query_db(query, data)


    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL(DATABASE).query_db(query)
        users = []
        for row in results:
            users.append(cls(row))
        return users

    @classmethod
    def get_all_workout(cls):
        query = """
        SELECT * FROM workouts JOIN users ON workouts.user_id = users.id
        JOIN typesof ON workouts.type_id= typesof.id;"""
        results = connectToMySQL(DATABASE).query_db(query)
        thisone_workout = []
        for row in results:
            thisone_workout.append(row)
        return thisone_workout

    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL(DATABASE).query_db(query, data)
        if results:
            return cls(results[0])
        return []

    @classmethod
    def get_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(DATABASE).query_db(query, data)
        if len(results) <1 :
            return False
        return cls(results[0])

    @classmethod
    def delete(cls, data):
        query = "DELETE FROM users WHERE id = %(id)s;"
        return connectToMySQL(DATABASE).query_db(query, data)
    
    @classmethod
    def show_all(cls):
        query = """
        SELECT * FROM users JOIN workouts ON users.id = workouts.user_id
        JOIN typesof ON typesof.id = workouts.type_id;
    """
        results = connectToMySQL(DATABASE).query_db(query)
        workout_plans = []
        # print (results)
        print(workout_plans)
        for row in results:
            this_workout = cls(row)
            data= {


                # 'created_at': row['workoutrs.created_at'],
                # 'updated_at': row['users.updated_at'],
                'id': row['workouts.id'],
                "created_at": row['workouts.created_at'],
                "updated_at": row['workouts.updated_at'],
                **row

            }
            this_user = workout_model.Workout(data)
            
            this_workout.workout_plan = this_user
            workout_plans.append(this_workout)
            print(this_workout)
            return workout_plans
        return results

    @staticmethod
    def is_valid(users):
            is_valid = True
            query = "SELECT * FROM users WHERE email = %(email)s;"
            results = connectToMySQL(DATABASE).query_db(query,users)
            if len(users['email']) <1 :
                flash("Email is required" , "register")
                is_valid = False
            if len(results) >= 1:
                flash("Email already taken" , "register")
                is_valid=False
            elif not EMAIL_REGEX.match(users['email']):
                flash("Invalid Email!", "register")
                is_valid=False
            if len(users['first_name']) <3:
                flash('First name must be 3 characters minimum!', "register")
                is_valid = False
            if len(users['last_name']) <3:
                flash(' Last name is required!', 'register')
                is_valid = False
            if len(users['password']) < 8:
                flash("Password must be 8 characters long", 'register')
                is_valid= False
            if not users['password'] == users['confirm']:
                flash("Passwords does not match", "register")
                is_valid= False
            return is_valid
        