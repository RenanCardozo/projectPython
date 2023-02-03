from flask_app import app
from flask import render_template, redirect, request, url_for, flash,session
from flask_app.controllers import users_controller, workouts_controller
from flask_app.model.user_model import User
from flask_app.model.workout_model import Workout
from flask_app.model.type_model import Type







@app.route('/dashboard/workout/<int:id>')
def dashboard_workout(id):
    if not 'user_id' in session:
        return redirect(url_for('login'))

    data={
        'id': session['user_id']

    }
    users = User.get_by_id(data)
    one_type = Type.get_by_id({'id':id})
    
    return render_template('workout_view.html', users=users, one_type=one_type)


