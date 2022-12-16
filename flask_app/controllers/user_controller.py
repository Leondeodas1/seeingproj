from flask_app import app
from flask import render_template,request, redirect,session
from flask_app.models import user
from datetime import datetime
from flask_app.models import sighting
dateFormat = "%m/%d/%Y %I:%M %p"



@app.route('/home') 
def dashboard():
    if 'users_id' in session:
        return render_template('dashboard.html',current_user = user.users.get_one({'id': session["users_id"]}), all = sighting.sighting.show_all_sighting())
    return redirect('/')

@app.route('/report_a_sighting')
def get_new_sighting():
    if 'users_id' not in session:
        return redirect('/home')
    return render_template("new_sighting.html",current_user = user.users.get_one({'id': session["users_id"]}) )

@app.route('/add_sighting', methods = ['POST'])
def add_recipe():
    if 'users_id' not in session:
        return redirect('/home')
    if not sighting.sighting.validate_sighting(request.form):
        return redirect('/report_a_sighting')
    sighting.sighting.insert_sighting(request.form)
    print(request.form)
    return redirect('/home')


@app.route('/edit/<int:id>', methods=['get'])
def get_edit_html(id):
    if 'users_id' not in session:
        return redirect('/home')
    data = {
        "id": id
    }
    return render_template("edit.html", one = sighting.sighting.get_one(data),current_user = user.users.get_one({'id': session["users_id"]}) )


@app.route('/change_sighting/<int:id>', methods= ['POST'])
def edit(id):
    if 'users_id' not in session:
        return redirect('/home')
    if not sighting.sighting.validate_sighting(request.form):
        return redirect(f'/edit/{id}')
        
    sighting.sighting.edit(request.form)
    print(request.form)
    return redirect('/home')


@app.route('/view_sightings/<int:id>', methods = ['GET'])
def get_recipes(id):
    data = {
        "id" : id
    }
    return render_template("show_sighting.html",sightings_and_user = sighting.sighting.show_sightings_by_id(data),one = sighting.sighting.get_one(data))


@app.route('/delete/<int:id>', methods = ['get'])
def delete(id):
    if 'users_id' not in session:
        return redirect('/home')
    data = {
        "id" :id
    }
    sighting.sighting.delete_it(data)
    return redirect('/home')
    