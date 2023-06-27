from flask import Flask, render_template, request, redirect, request, session, flash
from flask_app import app
from flask_app.models.user import User
from flask_app.models.post import Post

from flask_bcrypt import Bcrypt        
bcrypt = Bcrypt(app)

@app.route("/")
def login_page():
    return render_template("login.html")

@app.route('/register/user', methods=["POST"])
def register():
    if not User.validate(request.form):
        return redirect('/')
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    print(pw_hash)
    data = {
        "first_name": request.form["first_name"],
        "last_name": request.form["last_name"],
        "password": pw_hash,
        "email": request.form["email"]
    }
    new_user_id=User.save(data)
    return redirect('/reg_success')

@app.route("/reg_success")
def reg_success():
    return render_template("reg_success.html")

@app.route('/login/user', methods=["POST"])
def login_user():
    user = User.get_by_email(request.form)
    if not User.validate_login(request.form):
        return redirect('/')
    # pw_hash = bcrypt.generate_password_hash(request.form['password'])
    # data = {
    #     "email": request.form["email"],
    #     "password": pw_hash
    # }
    # id=User.save(data)
    print(user)
    session['id'] = user.id
    session['first_name'] = user.first_name
    session['last_name'] = user.last_name
    session['email'] = user.email
    return redirect('/dojo_wall')

@app.route("/dojo_wall")
def dojo_wall():
    if 'id' in session:
        data = {
            'id': session['id']
        }
        all_posts = Post.get_all()
        return render_template("dojo_wall.html", user = User.get_by_id(data), posts=all_posts)
    else:
        # flash('Login Not Logged In')
        redirect('/')

@app.route("/logout")
def logout():
    session.clear()
    print("session cleared")
    return render_template("login.html")