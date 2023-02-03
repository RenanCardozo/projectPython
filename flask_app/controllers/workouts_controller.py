from flask_app import app
from flask import render_template, redirect, request, url_for, flash, session
from flask_app.controllers import users_controller, types_controller
from flask_app.model.user_model import User
from flask_app.model.workout_model import Workout
from flask_app.model.type_model import Type




@app.route('/GetFit/workouts')
def plans():
    return render_template('workout_preview.html')


@app.route('/GetFit/create_workout')
def create_workout():
    if 'user_id' not in session:
        return redirect('/logout')
    
    data= {
        'id': session['user_id']
        
    }
    users = User.get_by_id(data)
    types = Type.get_all()
    return render_template('create_workout.html' , users=users , types=types)


@app.route('/GetFit/new_workout', methods=['POST'])
def new_workout():
    print(request.form)
    type_of  = Type.save(request.form)
    for i in range(5):
        if request.form[f'workout_name{i}'] == "":
            break
        dict = {
            **request.form,
            'workout_name' : request.form[f'workout_name{i}'], 
            'sets': request.form[f'sets{i}'],
            'reps': request.form[f'reps{i}'],
            'pounds': request.form[f'pounds{i}'],
            'creator_id': session['user_id'],
            'type_id': type_of
        }
        Workout.save(dict)
    

    return redirect('/GetFit/dashboard' )

@app.route('/Getfit/edit')

