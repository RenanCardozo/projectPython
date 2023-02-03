from flask_app import app
from flask import render_template, redirect, request, url_for, flash, session
from flask_app.controllers import workouts_controller
from flask_bcrypt import Bcrypt
from flask_app.model.user_model import User
from flask_app.model.workout_model import Workout
from flask_app.model.type_model import Type


bcrypt = Bcrypt(app)


#================ Home Page ==================
@app.route('/')
def home_page():
    return render_template('index.html')



#================ Login Page==================

@app.route('/GetFit/login')
def login_page():
    if 'user_id' in session:
        return redirect('/GetFit/dashboard')
    return render_template('login_register.html')



#=====================Login Post Action====================
@app.route('/login', methods=['post'])
def login():
    users= User.get_by_email(request.form)
    if not users:
        flash("Invalid email", "login")
        return redirect('/GetFit/login')

    if not bcrypt.check_password_hash(users.password, request.form['password']):
        flash("invalid password", 'login')
        return redirect('/GetFit/login')
    
    session['user_id'] = users.id
    return redirect('/GetFit/dashboard')





#=====================Register Post Action====================
@app.route('/register', methods=['post'])
def register():
    if not User.is_valid(request.form):
        return redirect('/GetFit/login')
    data = {
        "first_name" : request.form['first_name'],
        "last_name" : request.form['last_name'],
        "email" : request.form['email'],
        "password" : bcrypt.generate_password_hash(request.form['password'])
    }
    user_id = User.save(data)
    print(user_id)
    session['user_id']= user_id
    return redirect('/GetFit/dashboard' )


#================ Dashboard==================

@app.route('/GetFit/dashboard')
def dashboard_page():
    if 'user_id' not in session:
        return redirect('/logout')
    data= {
        'id': session['user_id']
    }
    users = User.get_by_id(data)
    workout_day = Type.workout_list()
    logged_user = session['user_id']
    
    return render_template('dashboard.html', users = users, workout_day = workout_day, logged_user = logged_user)
    




#================ Logout==================
@app.route('/logout')
def logout():
    session.clear()
    
    return redirect('/')


