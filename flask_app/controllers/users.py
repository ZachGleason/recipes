from flask_app.models.user import User
from flask_app.models.recipe import Recipe
from crypt import methods
from flask import render_template, request, redirect, session, flash
from flask_app import app
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template("login.html")


@app.route('/register/user', methods=["POST"])
def register_user():
    if not User.validate_user(request.form):
        return redirect('/')
    data ={
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": bcrypt.generate_password_hash(request.form['password'])
    }
    id = User.save(data)
    session['user_id'] = id
    return redirect('/')


@app.route('/login', methods=["POST"])
def login():
    user = User.get_email(request.form)
    if not user:
        flash("Invalid Email","login")
        return redirect('/')
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash("Invalid Password","login")
        return redirect('/')
    session['user_id'] = user.id
    return redirect('/dashboard')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/logout')
    data ={
        'id': session['user_id']
    }
    return render_template("dashboard.html", user=User.get_by_id(data), recipes= Recipe.get_all_recipes(data))


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


@app.route('/create')
def create_recipe():
    return render_template("new_recipes.html")

@app.route('/recipes/new', methods=["POST"])
def new_recipe():
        data ={
        "name": request.form['name'],
        "description": request.form['description'],
        "instructions": request.form['instructions'],
        "user_id": session["user_id"]
    }
        Recipe.new_recipe(data)
        return redirect('/dashboard')

@app.route('/delete/<int:id>')
def delete_recipe(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    Recipe.delete_recipe(data)
    return redirect('/dashboard')

@app.route('/instructions/<int:id>')
def instructions(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    Recipe.one_recipe(data)
    return render_template("instructions.html")