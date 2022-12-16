from flask_app import app
from flask import render_template,request, redirect,session
from flask_app.models import user
from datetime import datetime
from flask_bcrypt import Bcrypt
from flask import flash
bcrypt = Bcrypt(app)
dateFormat = "%m/%d/%Y %I:%M %p"


@app.route('/') 
def index():
    return render_template('index.html')
    
@app.route('/register', methods = ['POST'])
def register():
        #validate user input
    if user.users.validate_create(request.form):
        # if valide saave to db
    #secure password to becrypt
        print(request.form['password'])
        pw_hash = bcrypt.generate_password_hash(request.form['password'])
        print(pw_hash)
        data = {
            'first_name': request.form['first_name'],
            'last_name': request.form['last_name'], 
            'email': request.form['email'],
            'password': pw_hash
        }

    #store the user in session
        session['users_id'] = user.users.save(data)
    # redirect to / home
        return redirect('/home')
    return redirect('/')
    
@app.route('/login', methods = ['POST'])
def login():
    #validate user input
    data = {"email" : request.form["email"]}
    user_in_db = user.users.get_by_email(data)
    if user_in_db:
        if bcrypt.check_password_hash(user_in_db.password, request.form['password']):
    # if valide saave to db
    #store the user in session
            session['users_id'] = user_in_db.id
    # redirect to / home
            return redirect('/home')
    flash("Invaid crediencals", 'regError')
    return redirect('/')

@app.route('/logout')
def logout():
    #clear session
    # print(session["users_id"])
    session.clear()
    # print(session["users_id"])
    # rediert to root route
    return redirect('/')