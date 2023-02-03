from flask_app import DATABASE
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.model import user_model, workout_model


class Type:
    def __init__(self, data):
        self.id = data['id']
        self.level = data['level']
        self.body_part = data['body_part']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.workouts = []
        self.workout= None

        

    
            
    @classmethod
    def save(cls,data):
        query = """
        INSERT INTO typesof (level, body_part) VALUES (%(level)s, %(body_part)s);
        """
        return connectToMySQL(DATABASE).query_db(query,data)
            
            
            
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM typesof;"
        # make sure to call the connectToMySQL function with the schema you are targeting.
        results = connectToMySQL(DATABASE).query_db(query)
        print(results)
        
        # Create an empty list to append our instances of friends
        types_instance = []
        print(types_instance)
        # Iterate over the db results and create instances of friends with cls.
        if results:  # queriees we make give results
            for row in results:
                this_type = cls(row)
                types_instance.append(this_type)
            return types_instance
        return False
        
    @classmethod
    def get_by_id(cls, data):
        # double join to grab the information from all 3 tables
        query = """
        SELECT * FROM typesof JOIN workouts ON typesof.id = workouts.type_id
        JOIN users ON users.id = workouts.creator_id WHERE typesof.id = %(id)s;
        """
        # results of the query
        results = connectToMySQL(DATABASE).query_db(query, data)
        # creates an instance of the Type class
        one_type = cls(results[0])
        # type class has a lot of workouts associated, so we iterate
        for row in results:
        
        # each row is going to have workout data AND creator data
            workout_data = {
                **row,
                "id" : row['workouts.id'],
                'created_at': row['workouts.created_at'],
                'updated_at': row['workouts.updated_at']
            }
        # each row is going to have creator data
            creator_data={
                **row,
                'id':   row['users.id'],
                'created_at': row['created_at'],
                'updated_at': row['updated_at']
            }
            # create the intance of a workout
            workout = workout_model.Workout(workout_data)
            # a workout HAS a creator a TYPE does NOT. so we associate the creator with the INSTANCE of workout.
            workout.creator = user_model.User(creator_data)
            # our workout instance is complete so we append it to the list of workouts for the type
            one_type.workouts.append(workout)
        # we return the type because we want to display the type object in the show one page
        return one_type
        
        
    @classmethod
    def workout_list(cls):
                # double join to grab the information from all 3 tables
        # SELECT * FROM typesof JOIN workouts ON typesof.id = workouts.type_id
        # JOIN users ON users.id = workouts.creator_id;
        query = """
        SELECT * FROM typesof;
        """
        # results of the query
        results = connectToMySQL(DATABASE).query_db(query)
        # creates an instance of the Type class
        all_type = []
        # type class has a lot of workouts associated, so we iterate
        for row in results:
            this_type = cls(row)
            
            query = """
            SELECT * FROM workouts JOIN users ON users.id= workouts.creator_id WHERE type_id = %(id)s;
            """
            result = connectToMySQL(DATABASE).query_db(query, row)
        # each row is going to have workout data AND creator data
            # workout_data = {
            #     **row,
            #     "id" : row['workouts.id'],
            #     'created_at': row['workouts.created_at'],
            #     'updated_at': row['workouts.updated_at']
            # }
        # each row is going to have creator data
            if result:
                creator_data={
                    **result[0],
                    'id':   result[0]['users.id'],
                    'first_name': result[0]['first_name'],
                    'last_name':result[0]['last_name'],
                    'created_at':result[0]['created_at'],
                    'updated_at': result[0]['updated_at']
                    
                }
            
                # create the intance of a workout
                workout = workout_model.Workout(result[0])
                # a workout HAS a creator a TYPE does NOT. so we associate the creator with the INSTANCE of workout.
                workout.creator = user_model.User(creator_data)
                this_type.workout_list = workout
                # our workout instance is complete so we append it to the list of workouts for the type
                all_type.append(this_type)
        
        

        # we return the type because we want to display the type object in the show one page
        return all_type